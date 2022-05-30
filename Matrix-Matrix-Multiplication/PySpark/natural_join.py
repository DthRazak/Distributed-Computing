#!/usr/bin/env python3

import argparse
import pandas as pd
from operator import add
from pyspark.sql import SparkSession


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', type=str, help="Input file",
                        metavar='filename', default="../input/data.txt")
    parser.add_argument('-o', type=str, help="Output file",
                        metavar='filename', default="../output/pyspark-result-via-natural-join.csv")

    args = parser.parse_args()

    spark = SparkSession \
        .builder \
        .appName('Matrix Matrix Multiplication via natural join') \
        .getOrCreate()

    input_data = spark.read.option("lineSep", "\n").text(args.i).rdd

    def mapper(element):
        data = list()

        # Each element contains:
        # Matrix (i, j, m_ij, [A | B])
        row, col, val, orig = element[0].split(';')

        # emit key-value pair: (j, ([A | B], i, val))
        if orig == "A":
            key = int(col)
            value = ('A', int(row), int(val))
        else:
            key = int(row)
            value = ('B', int(col), int(val))

        return key, value

    transformed_data = input_data \
        .map(mapper)

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

        for _, i, val_a in grouped_values['A']:
            for _, k, val_b in grouped_values['B']:
                key = (i, k)
                value = val_a * val_b

                data.append((key, value))

        return data

    matrix = transformed_data \
        .groupByKey() \
        .flatMap(reducer) \
        .reduceByKey(add)

    # Note: This output is only for testing on a single computer
    # Change it if necessary
    df = matrix.toDF().toPandas()
    df = pd.concat([pd.DataFrame([*df['_1']], index=df.index), df['_2']], axis=1)
    df.to_csv(args.o, sep=';', index=False, header=False)

    spark.stop()


if __name__ == "__main__":
    main()
