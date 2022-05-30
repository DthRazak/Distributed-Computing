#!/usr/bin/env python3

import sys


def main():
    current_key = None
    key = None
    current_count = 0

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        key, _ = key_value.split(';')

        if current_key == key:
            current_count += 1
        else:
            # emit key-value pair: (_, num)
            # if L = [] contains one and only one element
            if current_key is not None and current_count == 1:
                print(f"{current_key}")

            current_key = key
            current_count = 1

    if current_key == key and current_count == 1:
        # emit last key-value pair if needed
        print(f"{current_key}")


if __name__ == "__main__":
    main()
