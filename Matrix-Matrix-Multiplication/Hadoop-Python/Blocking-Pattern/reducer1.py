#!/usr/bin/env python3

import sys


def emit(grouped_values):
    sum_dict = dict()

    # compute values of x_im
    for a_i, a_j, a_val in grouped_values['A']:
        if a_i not in sum_dict.keys():
            sum_dict[a_i] = dict()
        for b_j, b_m, b_val in grouped_values['B']:
            if a_j == b_j:
                if b_m in sum_dict[a_i].keys():
                    sum_dict[a_i][b_m] += a_val * b_val
                else:
                    sum_dict[a_i][b_m] = a_val * b_val

    # emit key-value pair: ((i, m), x)
    # `|` separates key and value
    # `;` separates inner values
    for i in sum_dict.keys():
        for m in sum_dict[i].keys():
            print(f"{i};{m}|{sum_dict[i][m]}")


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
            orig, row, col, val = value.split(';')
            grouped_values[orig].append((int(row), int(col), int(val)))
        else:
            if current_key is not None:
                emit(grouped_values)

            current_key = key
            orig, row, col, val = value.split(';')
            grouped_values = {'A': [], 'B': []}
            grouped_values[orig].append((int(row), int(col), int(val)))

    if current_key == key:
        emit(grouped_values)


if __name__ == "__main__":
    main()
