#!/usr/bin/env python3

import re
import argparse
from operator import add
from pyspark.sql import SparkSession


def mapper(word):
    return word, 1


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', type=str, help="Input text file",
                        metavar='filename', default="../input/text.txt")
    parser.add_argument('-o', type=str, help="Output file",
                        metavar='filename', default="../output/pyspark-result.csv")

    args = parser.parse_args()

    spark = SparkSession\
        .builder\
        .appName('Word count')\
        .getOrCreate()

    lines = spark\
        .read\
        .text(args.i)\
        .rdd\
        .map(lambda r: r[0].strip())

    counts = lines\
        .flatMap(lambda line: re.findall(r"[\w']+", line.lower()))\
        .map(mapper)\
        .reduceByKey(add)

    # Note: This output is only for a test on one computer
    # Change it if necessary
    df = counts.toDF().toPandas()
    df.to_csv(args.o, sep=';', index=False, header=False)

    spark.stop()


if __name__ == "__main__":
    main()
