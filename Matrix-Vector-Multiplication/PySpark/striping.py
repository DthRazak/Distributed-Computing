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
                        metavar='filename', default="../output/pyspark-result-striping.csv")

    args = parser.parse_args()

    spark = SparkSession \
        .builder \
        .appName('Matrix Vector Multiplication with Striping Pattern') \
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
            i, j, m = [int(val) for val in values]
            stripe = int(j / GLOBAL_BETA.value)

            key = (i, stripe)
            value = (j, m)
            data.append((key, value))
        else:
            j, v = [int(val) for val in values]
            stripe = int(math.floor(j / GLOBAL_BETA.value))

            # replicate key-value pairs
            for i in range(N.value):
                key = (i, stripe)
                value = (j, v)
                data.append((key, value))

        return data

    transformed_data = input_data \
        .flatMap(mapper)

    def reducer(kvl):
        key, value_list = kvl
        values = [val for val in value_list]

        current_sum = 0
        for i in range(len(values)):
            index, val = values[i]
            for j in range(i + 1, len(values)):
                other_index, other_val = values[j]
                if index == other_index:
                    current_sum = current_sum + val * other_val

        return key[0], current_sum

    vector = transformed_data \
        .groupByKey() \
        .map(reducer) \
        .reduceByKey(add)

    # Note: This output is only for testing on a single computer
    # Change it if necessary
    df = vector.toDF().toPandas()
    df.to_csv(args.o, sep=';', index=False, header=False)

    spark.stop()


if __name__ == "__main__":
    main()
