#!/usr/bin/env python3

import sys


def main():
    current_key = None
    key = None
    current_sum = 0

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        key, value = key_value.split('|')
        value = int(value)

        if current_key == key:
            current_sum += value
        else:
            # emit key-value pair: (k, x), `;` acts as a separator
            if current_key is not None:
                print(f"{current_key};{current_sum}")

            current_key = key
            current_sum = value

    if current_key == key:
        # emit last key-value pair if needed
        print(f"{current_key};{current_sum}")


if __name__ == "__main__":
    main()
