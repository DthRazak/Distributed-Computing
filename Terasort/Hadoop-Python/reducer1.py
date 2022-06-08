#!/usr/bin/env python3

import sys


def emit(grouped_values):
    # sort pivots
    grouped_values['PIVOT'].sort()
    for val in grouped_values['OBJECT']:
        if val <= grouped_values['PIVOT'][0]:
            print(f'0|{val}')
        elif val > grouped_values['PIVOT'][-1]:
            print(f"{len(grouped_values['PIVOT'])}|{val}")
        else:
            idx = 1
            while idx < len(grouped_values['PIVOT']) and val >= grouped_values['PIVOT'][idx-1]:
                idx += 1
            print(f"{idx - 1}|{val}")


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
            # and group by OBJECT or PIVOT
            val_type, val = value.split(';')
            grouped_values[val_type].append(int(val))
        else:
            if current_key is not None:
                emit(grouped_values)

            current_key = key
            val_type, val = value.split(';')
            grouped_values = {'OBJECT': [], 'PIVOT': []}
            grouped_values[val_type].append(int(val))

    if current_key == key:
        emit(grouped_values)


if __name__ == "__main__":
    main()
