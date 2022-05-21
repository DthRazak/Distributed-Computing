#!/usr/bin/env python3

import lorem
import argparse


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-t', type=int, help="Number of texts",
                        metavar='num', default=10)
    parser.add_argument('-s', type=int, help="Number of sentences",
                        metavar='num', default=argparse.SUPPRESS)
    parser.add_argument('-p', type=int, help="Number of paragraphs",
                        metavar='num', default=argparse.SUPPRESS)
    parser.add_argument('-f', type=str, help="Write generated words to `filename`",
                        metavar='filename', default="input/text.txt")

    args = parser.parse_args()

    with open(args.f, 'w') as file:
        if hasattr(args, 's'):
            for i in range(args.s):
                file.write(lorem.sentence())
        elif hasattr(args, 'p'):
            for i in range(args.p):
                file.write(lorem.paragraph())
        else:
            for i in range(args.t):
                file.write(lorem.text())


if __name__ == "__main__":
    main()
