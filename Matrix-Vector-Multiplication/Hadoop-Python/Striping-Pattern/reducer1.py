#!/usr/bin/env python3

import sys


def aggregate_values(values):
    current_sum = 0
    for i in range(len(values)):
        index, val = values[i]
        for j in range(i+1, len(values)):
            other_index, other_val = values[j]
            if index == other_index:
                current_sum = current_sum + val * other_val
    return current_sum


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
                current_sum = aggregate_values(values)

                # emit key-value pair: (row coordinate, current sum), `;` acts as a separator
                row_coordinate = current_key.split(';')[0]
                print(f'{row_coordinate};{current_sum}')

            current_key = key
            values = [tuple(int(num) for num in value.split(';'))]

    if current_key == key:
        # emit last key-value pair if needed
        current_sum = aggregate_values(values)

        row_coordinate = current_key.split(';')[0]
        print(f'{row_coordinate};{current_sum}')


if __name__ == "__main__":
    main()
