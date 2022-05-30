#!/usr/bin/env python3

import sys


def emit(key, p, grouped_values):
    # sort values to simplify search in lists
    grouped_values['A'].sort(key=lambda tup: tup[0])
    grouped_values['B'].sort(key=lambda tup: tup[0])

    # we `connect` the two values in each list sharing a same j
    # and emit key-value pair: ((i, k), x), `;` acts as a separator
    current_sum = 0
    for j in range(p):
        val_a = grouped_values['A'][j][1]
        val_b = grouped_values['B'][j][1]
        current_sum += val_a * val_b
    print(f'{key};{current_sum}')


def main():
    # We assume that required arguments are passed to mapper
    p = int(sys.argv[1])

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
                emit(current_key, p, grouped_values)

            current_key = key
            orig, row_col, val = value.split(';')
            grouped_values = {'A': [], 'B': []}
            grouped_values[orig].append((int(row_col), int(val)))

    if current_key == key:
        emit(current_key, p, grouped_values)


if __name__ == "__main__":
    main()
