#!/usr/bin/env python3

import sys


def main():
    for line in sys.stdin:
        # Just emit key-value pair: (word, number) `;` acts as a separator
        print(line, end='')


if __name__ == "__main__":
    main()
