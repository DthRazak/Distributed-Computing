#!/usr/bin/env python3

import sys


def emit(key, grouped_values):
    Ni = len(grouped_values)
    print(f"{key}|CARD;{key};{Ni}")

    for s in grouped_values:
        print(f"{key}|{s}")


def main():
    current_key = None
    key = None
    grouped_values = list()

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        key, value = key_value.split('|')

        if current_key == key:
            # collect list L = [s1, s2, ...]
            grouped_values.append(int(value))
        else:
            if current_key is not None:
                emit(current_key, grouped_values)

            current_key = key
            grouped_values = [int(value)]

    if current_key == key:
        emit(current_key, grouped_values)


if __name__ == "__main__":
    main()
