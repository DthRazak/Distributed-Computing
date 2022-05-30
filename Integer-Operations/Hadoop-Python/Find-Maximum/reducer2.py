#!/usr/bin/env python3

import sys


def main():
    max_value = float('-inf')

    # there must be only one key-value_list
    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        _, value = key_value.split(';')
        max_value = max(max_value, int(value))

    print(f"{max_value}")


if __name__ == "__main__":
    main()
