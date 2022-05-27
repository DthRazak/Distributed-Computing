#!/usr/bin/env python3

import sys
import math


def main():
    # We assume that required arguments are passed to mapper
    n, block_size = [int(num) for num in sys.argv[1:3]]

    # Each chunk contains:
    # Matrix element (i, j, m_ij, [A | B])
    for chunk in sys.stdin:
        row, col, val, orig = chunk.split(';')
        row, col = int(row), int(col)

        # replicate and emit key-value pair: ((s, t, k), ([A | B], i, j, val))
        # `|` separates key and value
        # `;` separates inner values
        if orig[0] == "A":
            s = int(math.floor(row / block_size))
            t = int(math.floor(col / block_size))

            for k in range(int(n / block_size)):
                print(f"{s};{t};{k}|A;{row};{col};{val}")
        else:
            t = int(math.floor(row / block_size))
            k = int(math.floor(col / block_size))

            for s in range(int(n / block_size)):
                print(f"{s};{t};{k}|B;{row};{col};{val}")


if __name__ == "__main__":
    main()
