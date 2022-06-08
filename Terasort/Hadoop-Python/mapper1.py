#!/usr/bin/env python3

import sys
import numpy as np


def main():
    # We assume that required arguments are passed to mapper
    p, N = [int(num) for num in sys.argv[1:3]]

    # Each chunk contains one number
    for chunk in sys.stdin:
        rnd_num = int(np.random.default_rng().uniform(0, 100, 1))

        key = rnd_num % p
        value = int(chunk)

        # emit key-value pair: (key, (OBJECT, value))
        # `|` separates key and value
        # `;` separates inner values
        print(f"{key}|OBJECT;{value}")

        alpha = np.random.default_rng().uniform(0, 1, 1)
        if alpha <= (p - 1) / N:
            # pivots replications
            for w in range(p):
                print(f"{w}|PIVOT;{value}")


if __name__ == "__main__":
    main()
