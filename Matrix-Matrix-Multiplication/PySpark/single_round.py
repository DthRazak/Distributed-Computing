#!/usr/bin/env python3

import argparse
import pandas as pd
from operator import add
from pyspark.sql import SparkSession


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', nargs=3, type=int, help="Size of matrices A x B",
                        default=[20, 20, 20], metavar=('N', 'P', 'M'))
    parser.add_argument('-i', type=str, help="Input file",
                        metavar='filename', default="../input/data.txt")
    parser.add_argument('-o', type=str, help="Output file",
                        metavar='filename', default="../output/pyspark-result-single-round.csv")

    args = parser.parse_args()

    spark = SparkSession \
        .builder \
        .appName('Matrix Matrix Multiplication - single round') \
        .getOrCreate()

    N = spark.sparkContext.broadcast(args.s[0])
    P = spark.sparkContext.broadcast(args.s[1])
    M = spark.sparkContext.broadcast(args.s[2])

    input_data = spark.read.option("lineSep", "\n").text(args.i).rdd

    def mapper(element):
        data = list()

        # Each element contains:
        # Matrix (i, j, m_ij, [A | B])
        row, col, val, orig = element[0].split(';')

        # replicate emit key-value pair: ((i, k), ([A | B], j, val))
        if orig[0] == "A":
            for k in range(M.value):
                key = (int(row), k)
                value = ('A', int(col), int(val))

                data.append((key, value))
        else:
            for i in range(N.value):
                key = (i, int(col))
                value = ('B', int(row), int(val))

                data.append((key, value))

        return data

    transformed_data = input_data \
        .flatMap(mapper)

    def reducer(kvl):

        key, value_list = kvl
        values = [val for val in value_list]
        grouped_values = {'A': [], 'B': []}
        for value in values:
            if value[0] == 'A':
                grouped_values['A'].append(value)
            else:
                grouped_values['B'].append(value)

        grouped_values['A'].sort(key=lambda tup: tup[1])
        grouped_values['B'].sort(key=lambda tup: tup[1])

        current_sum = 0
        for j in range(P.value):
            val_a = grouped_values['A'][j][2]
            val_b = grouped_values['B'][j][2]
            current_sum += val_a * val_b

        return key, current_sum

    matrix = transformed_data \
        .groupByKey() \
        .map(reducer)

    # Note: This output is only for testing on a single computer
    # Change it if necessary
    df = matrix.toDF().toPandas()
    df = pd.concat([pd.DataFrame([*df['_1']], index=df.index), df['_2']], axis=1)
    df.to_csv(args.o, sep=';', index=False, header=False)

    spark.stop()


if __name__ == "__main__":
    main()
