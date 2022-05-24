#!/usr/bin/env python3

import sys
import math


def main():
    # We assume that required arguments are passed to mapper
    n, num_stripes = [int(num) for num in sys.argv[1:3]]

    # Each chunk contains:
    # Matrix element (i, j, m_ij) or
    # Vector element (j, v_j)
    for chunk in sys.stdin:
        elements = chunk.split(';')

        if len(elements) == 3:
            # Matrix value
            i, j, m = elements
            m = int(m)
            stripe = int(math.floor(int(j) / num_stripes))

            # emit key-value pair: ((i, stripe), (j, m_ij))
            # `|` separates key and value
            # `;` separates inner values
            print(f"{i};{stripe}|{j};{m}")
        else:
            # Vector value
            j, v = elements
            v = int(v)
            stripe = int(math.floor(int(j) / num_stripes))

            # replicate and emit key-value pair: ((i, stripe), (i, v_i))
            # `|` separates key and value
            # `;` separates inner values
            for i in range(n):
                print(f"{i};{stripe}|{j};{v}")


if __name__ == "__main__":
    main()
