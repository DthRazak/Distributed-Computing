#!/usr/bin/env python3


import sys


def main():
    current_key = None
    key = None

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        key, _ = key_value.split(';')

        if current_key != key:
            # emit key-value pair: (_, num)
            # for each key-value_list we emit only one value
            if current_key is not None:
                print(f"{current_key}")

            current_key = key

    if current_key == key:
        # emit last key-value pair if needed
        print(f"{current_key}")


if __name__ == "__main__":
    main()
