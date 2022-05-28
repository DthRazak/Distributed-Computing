#!/usr/bin/env python3

import sys
import random


def main():
    # We assume that required arguments are passed to mapper
    num_split = int(sys.argv[1])

    # Each chunk contains one number
    for chunk in sys.stdin:
        key = random.randint(1, num_split)
        num = int(chunk)

        # just emit key-value pair: (random key, num), `;` acts as a separator
        print(f"{key};{num}")


if __name__ == "__main__":
    main()
