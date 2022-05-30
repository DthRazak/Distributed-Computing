#!/usr/bin/env python3

import math
import argparse
import random
from operator import add
from pyspark.sql import SparkSession


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', type=int, help="Number of splits",
                        metavar='SPLIT_NUM', default=10)
    parser.add_argument('-i', type=str, help="Input text file",
                        metavar='filename', default="../input/data.txt")
    parser.add_argument('-o', type=str, help="Output file",
                        metavar='filename', default="../output/pyspark-find-maximum.csv")

    args = parser.parse_args()

    spark = SparkSession \
        .builder \
        .appName('Find maximum') \
        .getOrCreate()

    SPLIT_NUM = spark.sparkContext.broadcast(args.n)

    input_data = spark.read.option("lineSep", "\n").text(args.i).rdd

    def mapper(element):
        key = random.randint(1, SPLIT_NUM.value)
        num = int(element[0])

        return key, num

    transformed_data = input_data \
        .map(mapper)

    maximum = transformed_data \
        .reduceByKey(max) \
        .values() \
        .reduce(lambda v1, v2: max(v1, v2))

    with open(args.o, 'w') as file:
        file.write(str(maximum))

    spark.stop()


if __name__ == "__main__":
    main()
