#!/usr/bin/env python3

import sys


def main():
    # We assume that required arguments are passed to mapper
    n, m = [int(num) for num in sys.argv[1:3]]

    # Each chunk contains:
    # Matrix element (i, j, m_ij, [A | B])
    for chunk in sys.stdin:
        row, col, val, orig = chunk.split(';')

        # replicate emit key-value pair: ((i, k), ([A | B], j, val))
        # `|` separates key and value
        # `;` separates inner values
        if orig[0] == "A":
            for k in range(m):
                print(f"{row};{k}|{orig[0]};{col};{val}")
        else:
            for i in range(n):
                print(f"{i};{col}|{orig[0]};{row};{val}")


if __name__ == "__main__":
    main()
