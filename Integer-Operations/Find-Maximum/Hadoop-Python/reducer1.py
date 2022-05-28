#!/usr/bin/env python3

import sys


def main():
    current_key = None
    key = None
    max_value = float('-inf')

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        key, value = key_value.split(';')

        if current_key == key:
            max_value = max(max_value, int(value))
        else:
            # emit all max values to the same reducer in 2nd round
            # `;` separates key and value (0, value)
            if current_key is not None:
                print(f"0;{max_value}")

            max_value = int(value)
            current_key = key

    if current_key == key:
        print(f"0;{max_value}")


if __name__ == "__main__":
    main()
