#!/usr/bin/env python3

import sys


def emit(values):
    row_values = dict()
    for i in range(len(values)):
        # for each matrix element (size: 3)
        if len(values[i]) == 3:
            mat_row, mat_col, mat_val = values[i]

            if mat_row not in row_values.keys():
                row_values[mat_row] = 0

            for j in range(len(values)):
                # for each vector element (size: 2)
                if len(values[j]) == 2:
                    vec_row, vec_val = values[j]
                    if mat_col == vec_row:
                        row_values[mat_row] += mat_val * vec_val

    for key_value in row_values.items():
        # emit key-value pair: (row coordinate, current sum), `;` acts as a separator
        print(f'{key_value[0]};{key_value[1]}')


def main():
    current_key = None
    key = None
    values = list()

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        key, value = key_value.split('|')

        if current_key == key:
            # collect list L = [( , ), ( , ), ... ( , )]
            values.append(tuple(int(num) for num in value.split(';')))
        else:
            if current_key is not None:
                emit(values)

            current_key = key
            values = [tuple(int(num) for num in value.split(';'))]

    if current_key == key:
        emit(values)


if __name__ == "__main__":
    main()
