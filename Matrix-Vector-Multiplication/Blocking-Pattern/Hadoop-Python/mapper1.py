#!/usr/bin/env python3

import sys
import math


def main():
    # We assume that required arguments are passed to mapper
    n, block_size = [int(num) for num in sys.argv[1:3]]

    # Each chunk contains:
    # Matrix element (i, j, m_ij) or
    # Vector element (j, v_j)
    for chunk in sys.stdin:
        elements = chunk.split(';')

        if len(elements) == 3:
            # Matrix value
            i, j, m = [int(num) for num in elements]
            s = int(math.floor(i / block_size))
            t = int(math.floor(j / block_size))

            # emit key-value pair: ((s, t), (i, j, m_ij))
            # `|` separates key and value
            # `;` separates inner values
            print(f"{s};{t}|{i};{j};{m}")
        else:
            # Vector value
            j, v = [int(num) for num in elements]
            t = int(math.floor(j / block_size))

            # replicate and emit key-value pair: ((s, t), (j, v_j))
            # `|` separates key and value
            # `;` separates inner values
            for s in range(int(n / block_size)):
                print(f"{s};{t}|{j};{v}")


if __name__ == "__main__":
    main()
