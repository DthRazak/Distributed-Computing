#!/usr/bin/env python3

import math
import argparse
from operator import add
from pyspark.sql import SparkSession


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', type=str, help="Input text file",
                        metavar='filename', default="../input/data.txt")
    parser.add_argument('-o', type=str, help="Output file",
                        metavar='filename', default="../output/pyspark-find-distinct.csv")

    args = parser.parse_args()

    spark = SparkSession \
        .builder \
        .appName('Find distinct') \
        .getOrCreate()

    input_data = spark.read.option("lineSep", "\n").text(args.i).rdd

    def mapper(element):
        number = int(element[0])

        return number, 1

    transformed_data = input_data \
        .map(mapper)

    distinct_values = transformed_data \
        .reduceByKey(add) \
        .filter(lambda kv: kv[1] == 1)\

    # Note: This output is only for testing on a single computer
    # Change it if necessary
    df = distinct_values.toDF().toPandas().iloc[:, :1]
    df.to_csv(args.o, sep=';', index=False, header=False)

    spark.stop()


if __name__ == "__main__":
    main()
