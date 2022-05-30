#!/usr/bin/env python3

import math
import argparse
import pandas as pd
from operator import add
from pyspark.sql import SparkSession


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', type=int, help="Size of square matrix",
                        metavar='N', default=20)
    parser.add_argument('-b', type=int, help="Number of bands",
                        metavar='BAND_NUMBER', default=5)
    parser.add_argument('-i', type=str, help="Input file",
                        metavar='filename', default="../input/data.txt")
    parser.add_argument('-o', type=str, help="Output file",
                        metavar='filename', default="../output/pyspark-banding.csv")

    args = parser.parse_args()

    spark = SparkSession \
        .builder \
        .appName('Matrix Matrix Multiplication with Blocking Pattern') \
        .getOrCreate()

    N = spark.sparkContext.broadcast(args.n)
    BAND_NUM = spark.sparkContext.broadcast(args.b)

    input_data = spark.read.option("lineSep", "\n").text(args.i).rdd

    def mapper(element):
        data = list()

        # Each element contains:
        # Matrix (i, j, m_ij, [A | B])
        row, col, val, orig = element[0].split(';')
        row, col, val = int(row), int(col), int(val)

        # replicate emit key-value pair: ((i, k), ([A | B], j, val))
        if orig[0] == "A":
            g_i = int(math.floor(row / BAND_NUM.value))

            for b in range(BAND_NUM.value):
                key = (g_i, b)
                value = ('A', row, col, val)

                data.append((key, value))
        else:
            g_j = int(math.floor(col / BAND_NUM.value))

            for b in range(BAND_NUM.value):
                key = (b, g_j)
                value = ('B', row, col, val)

                data.append((key, value))

        return data

    transformed_data = input_data \
        .flatMap(mapper)

    def reducer(kvl):
        data = list()

        key, value_list = kvl
        values = [val for val in value_list]
        grouped_values = {'A': [], 'B': []}
        for value in values:
            if value[0] == 'A':
                grouped_values['A'].append(value)
            else:
                grouped_values['B'].append(value)

        sum_dict = dict()

        # compute values of x_im
        for _, a_i, a_j, a_val in grouped_values['A']:
            if a_i not in sum_dict.keys():
                sum_dict[a_i] = dict()
            for _, b_j, b_m, b_val in grouped_values['B']:
                if a_j == b_j:
                    if b_m in sum_dict[a_i].keys():
                        sum_dict[a_i][b_m] += a_val * b_val
                    else:
                        sum_dict[a_i][b_m] = a_val * b_val

        # collect key-value pair: ((i, m), x)
        for i in sum_dict.keys():
            for m in sum_dict[i].keys():
                key = (i, m)
                value = sum_dict[i][m]

                data.append((key, value))

        return data

    matrix = transformed_data \
        .groupByKey() \
        .flatMap(reducer)

    # Note: This output is only for testing on a single computer
    # Change it if necessary
    df = matrix.toDF().toPandas()
    df = pd.concat([pd.DataFrame([*df['_1']], index=df.index), df['_2']], axis=1)
    df.to_csv(args.o, sep=';', index=False, header=False)

    spark.stop()


if __name__ == "__main__":
    main()
