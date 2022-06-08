#!/usr/bin/env python3

import random
import argparse


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', type=int, help="Number of integers",
                        metavar='num', default=1000)
    parser.add_argument('-r', nargs=2, type=int, help="Range of random numbers",
                        default=[0, 500], metavar=('a', 'b'))
    parser.add_argument('-f', type=str, help="Write generated numbers to `filename`",
                        metavar='filename', default="input/data.txt")

    args = parser.parse_args()
    a, b = args.r

    numbers = list()
    unique_num_count = int((b - a) / 3)
    unique_num = set([random.randint(a, b) for i in range(unique_num_count)])
    unique_num_list = list(unique_num)

    for i in range(args.n - len(unique_num)):
        num = random.randint(a, b)
        while num in unique_num:
            num = random.randint(a, b)

        numbers.append(num)

    for num in unique_num_list:
        numbers.append(num)

    random.shuffle(numbers)

    with open(args.f, 'w') as file:
        for num in numbers:
            file.write(f'{num}\n')


if __name__ == "__main__":
    main()
