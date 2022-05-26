#!/usr/bin/env python

import numpy as np
import argparse


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-s', nargs=3, type=int, help="Size of matrices A x B",
                        default=[20, 20, 20], metavar=('m', 'n', 'k'))
    parser.add_argument('-f', type=str, help="Write generated matrices to `filename`",
                        metavar='filename', default="./input/data.txt")

    args = parser.parse_args()
    m, n, k = args.s

    A = np.rint(np.random.rand(m, n) * 10).astype(int)
    B = np.rint(np.random.rand(n, k) * 10).astype(int)

    with open(args.f, 'w') as file:
        for row in range(m):
            for col in range(n):
                val = A[row, col]
                file.write(f'{row};{col};{val};A\n')

        for row in range(n):
            for col in range(k):
                val = B[row, col]
                file.write(f'{row};{col};{val};B\n')


if __name__ == "__main__":
    main()
