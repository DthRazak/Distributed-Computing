#!/usr/bin/env python3

import sys


def main():
    # Each chunk contains:
    # Matrix element (i, j, m_ij, [A | B])
    for chunk in sys.stdin:
        row, col, val, orig = chunk.split(';')

        # emit key-value pair: (j, ([A | B], i, val))
        # `|` separates key and value
        # `;` separates inner values
        if orig[0] == "A":
            print(f"{col}|A;{row};{val}")
        else:
            print(f"{row}|B;{col};{val}")


if __name__ == "__main__":
    main()
