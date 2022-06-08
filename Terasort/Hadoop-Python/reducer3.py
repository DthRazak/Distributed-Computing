#!/usr/bin/env python3

import sys


def emit(key, grouped_values):
    grouped_values['OBJECTS'].sort()

    key = int(key)
    R = 1
    if key != 0:
        for i in range(key):
            R += grouped_values['CARD'][i]

    for pos, val in enumerate(grouped_values['OBJECTS']):
        print(f"{R + pos};{val}")


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
            values = value.split(';')
            if len(values) == 2:
                grouped_values['OBJECTS'].append(int(values[1]))
            else:
                grouped_values['CARD'][int(values[1])] = int(values[2])
        else:
            if current_key is not None:
                emit(current_key, grouped_values)

            current_key = key
            values = value.split(';')
            grouped_values = {'OBJECTS': [], 'CARD': {}}
            if len(values) == 2:
                grouped_values['OBJECTS'].append(int(values[1]))
            else:
                grouped_values['CARD'][int(values[1])] = int(values[2])

    if current_key == key:
        emit(current_key, grouped_values)


if __name__ == "__main__":
    main()
