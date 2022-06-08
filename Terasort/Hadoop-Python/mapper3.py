#!/usr/bin/env python3

import sys


def main():
    # We assume that required arguments are passed to mapper
    eta = int(sys.argv[1])

    for chunk in sys.stdin:
        key, values = chunk.split('|')
        values = values.split(';')

        if len(values) == 3:
            i, Ni = int(values[1]), int((values[2]))
            for w in range(eta):
                print(f"{w}|CARD;{i};{Ni}")
        else:
            s = int(values[0])
            print(f"{key}|OBJECT;{s}")


if __name__ == "__main__":
    main()
