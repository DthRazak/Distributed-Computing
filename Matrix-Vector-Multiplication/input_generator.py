#!/usr/bin/env python3

import argparse
import numpy as np


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', type=int, help="Size of square matrix and vector (max: 10000)",
                        metavar='num', default=20)
    parser.add_argument('-f', type=str, help="Write generated words to `filename`",
                        metavar='filename', default="input/data.txt")

    args = parser.parse_args()

    mat = np.rint(np.random.rand(args.n, args.n) * 10).astype(int)
    vec = np.rint(np.random.rand(args.n) * 10).astype(int)

    with open(args.f, 'w') as file:
        for i in range(args.n):
            for j in range(args.n):
                file.write(f'{i};{j};{mat[i, j]}\n')

        for i in range(args.n):
            file.write(f'{i};{vec[i]}\n')


if __name__ == "__main__":
    main()
