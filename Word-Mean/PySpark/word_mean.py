#!/usr/bin/env python3

import argparse
from pyspark.sql import SparkSession


def mapper(element):
    # Each input element: word;number
    values = element.split(';')
    return values[0], int(values[1])


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', type=str, help="Input text file",
                        metavar='filename', default="../input/text.txt")
    parser.add_argument('-o', type=str, help="Output file",
                        metavar='filename', default="../output/pyspark-result.csv")

    args = parser.parse_args()

    spark = SparkSession \
        .builder \
        .appName('Word mean') \
        .getOrCreate()

    lines = spark \
        .read \
        .text(args.i) \
        .rdd \
        .map(lambda r: r[0].strip())

    # Accumulating sum and count for a given key
    seq_fun = (lambda v1, v2: (v1[0] + v2, v1[1] + 1))
    comb_fun = (lambda v1, v2: (v1[0] + v2[0], v1[1] + v2[0]))

    mean_values = lines \
        .map(mapper) \
        .aggregateByKey((0, 0), seq_fun, comb_fun) \
        .mapValues(lambda val: round(val[0] / val[1], 2))

    # Note: This output is only for testing on a single computer
    # Change it if necessary
    df = mean_values.toDF().toPandas()
    df.to_csv(args.o, sep=';', index=False, header=False)

    spark.stop()


if __name__ == "__main__":
    main()
