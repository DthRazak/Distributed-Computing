#!/usr/bin/env python3

import sys


def main():
    for key_value in sys.stdin:
        # Just emit key-value pair: (i, x) `;` acts as a separator
        print(key_value, end='')


if __name__ == "__main__":
    main()
