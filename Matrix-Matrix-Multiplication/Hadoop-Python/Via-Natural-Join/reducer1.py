#!/usr/bin/env python3

import sys


def emit(grouped_values):
    for i, val_a in grouped_values['A']:
        for k, val_b in grouped_values['B']:
            # emit key-value pair: ((i, k), a * b)
            # `|` separates key and value
            # `;` separates inner values
            print(f'{i};{k}|{val_a * val_b}')


def main():
    current_key = None
    key = None
    grouped_values = dict()

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        key, value = key_value.split('|')

        if current_key == key:
            # collect list L = [( , ), ( , ), ... ( , )]
            # and group by matrix A or B
            orig, row_col, val = value.split(';')
            grouped_values[orig].append((int(row_col), int(val)))
        else:
            if current_key is not None:
                emit(grouped_values)

            current_key = key
            orig, row_col, val = value.split(';')
            grouped_values = {'A': [], 'B': []}
            grouped_values[orig].append((int(row_col), int(val)))

    if current_key == key:
        emit(grouped_values)


if __name__ == "__main__":
    main()
