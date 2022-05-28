#!/usr/bin/env python3

import sys


def main():
    # Each chunk contains one number
    for chunk in sys.stdin:
        num = int(chunk)

        # just emit key-value pair: (num, num), `;` acts as a separator
        print(f"{num};{num}")


if __name__ == "__main__":
    main()
