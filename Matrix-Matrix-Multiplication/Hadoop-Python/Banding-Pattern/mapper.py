#!/usr/bin/env python3

import sys
import math


def main():
    # We assume that required arguments are passed to mapper
    n, band_num = [int(num) for num in sys.argv[1:3]]

    # Each chunk contains:
    # Matrix element (i, j, m_ij, [A | B])
    for chunk in sys.stdin:
        row, col, val, orig = chunk.split(';')
        row, col = int(row), int(col)

        # replicate and emit key-value pair: ([(g_i, b) | (b, g_j)], ([A | B], i, j, val))
        # `|` separates key and value
        # `;` separates inner values
        if orig[0] == "A":
            g_i = int(math.floor(row / band_num))

            for b in range(band_num):
                print(f"{g_i};{b}|A;{row};{col};{val}")
        else:
            g_j = int(math.floor(col / band_num))

            for b in range(band_num):
                print(f"{b};{g_j}|B;{row};{col};{val}")


if __name__ == "__main__":
    main()
