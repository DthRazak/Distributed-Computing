#!/usr/bin/env python3

import sys


def main():
    for key_value in sys.stdin:
        # just emit key-value pair: ((i, m), x)
        # `|` separates key and value
        # `;` separates inner values
        print(key_value, end='')


if __name__ == "__main__":
    main()
