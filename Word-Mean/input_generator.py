#!/usr/bin/env python3

import random
import argparse
import requests


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', type=int, help="Number of words (max: 10000)",
                        metavar='num', default=1000, choices=range(10, 10000))
    parser.add_argument('-r', nargs=2, type=int, help="Range of random numbers",
                        default=[0, 100], metavar=('a', 'b'))
    parser.add_argument('-f', type=str, help="Write generated words to `filename`",
                        metavar='filename', default="input/text.txt")

    args = parser.parse_args()
    a, b = args.r

    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"

    response = requests.get(word_site)
    words = response.content.decode('utf-8').split()
    random.shuffle(words)

    # make words repeat
    words = words[:int(args.n / 10)]

    with open(args.f, 'w') as file:
        for i in range(args.n):
            file.write(f'{random.choice(words)};{random.randint(a, b)}\n')


if __name__ == "__main__":
    main()
