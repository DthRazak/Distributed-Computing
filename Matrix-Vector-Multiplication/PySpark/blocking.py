#!/usr/bin/env python3

import math
import argparse
from operator import add
from pyspark.sql import SparkSession


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', type=int, help="Size of vector",
                        metavar='N', default="20")
    parser.add_argument('-B', type=int, help="Size of stripe",
                        metavar='BETA', default="5")
    parser.add_argument('-i', type=str, help="Input text file",
                        metavar='filename', default="../input/mat_20.txt")
    parser.add_argument('-o', type=str, help="Output file",
                        metavar='filename', default="../output/pyspark-result-blocking.csv")

    args = parser.parse_args()

    spark = SparkSession \
        .builder \
        .appName('Matrix Vector Multiplication with Blocking Pattern') \
        .getOrCreate()

    GLOBAL_BETA = spark.sparkContext.broadcast(args.B)
    N = spark.sparkContext.broadcast(args.n)

    input_data = spark.read.option("lineSep", "\n").text(args.i).rdd

    def mapper(element):
        data = list()

        # Each element contains:
        # Matrix (i, j, m_ij) or vector (j, v_j) value

        values = element.value.split(';')
        if len(values) == 3:
            i, j, m = [int(num) for num in values]
            s = int(math.floor(i / GLOBAL_BETA.value))
            t = int(math.floor(j / GLOBAL_BETA.value))

            key = (s, t)
            value = (i, j, m)
            data.append((key, value))
        else:
            j, v = [int(num) for num in values]
            t = int(math.floor(j / GLOBAL_BETA.value))

            # replicate key-value pairs
            for s in range(int(N.value / GLOBAL_BETA.value)):
                key = (s, t)
                value = (j, v)
                data.append((key, value))

        return data

    transformed_data = input_data \
        .flatMap(mapper)

    def reducer(kvl):
        data = list()
        key, value_list = kvl
        values = [val for val in value_list]

        row_values = dict()
        for i in range(len(values)):
            # for each matrix element (size: 3)
            if len(values[i]) == 3:
                mat_row, mat_col, mat_val = values[i]

                if mat_row not in row_values.keys():
                    row_values[mat_row] = 0

                for j in range(len(values)):
                    # for each vector element (size: 2)
                    if len(values[j]) == 2:
                        vec_row, vec_val = values[j]
                        if mat_col == vec_row:
                            row_values[mat_row] += mat_val * vec_val

        for key_value in row_values.items():
            # collect key-value pair: (row coordinate, current sum)
            data.append((key_value[0], key_value[1]))

        return data

    vector = transformed_data \
        .groupByKey() \
        .flatMap(reducer) \
        .reduceByKey(add)

    # Note: This output is only for testing on a single computer
    # Change it if necessary
    df = vector.toDF().toPandas()
    df.to_csv(args.o, sep=';', index=False, header=False)

    spark.stop()


if __name__ == "__main__":
    main()
