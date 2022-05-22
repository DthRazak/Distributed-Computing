#!/usr/bin/env python3


import sys


def main():
    current_word = None
    word = None
    current_sum = 0
    count = 0

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        word, num = key_value.split(';')
        num = int(num)

        if current_word == word:
            current_sum += num
            count += 1
        else:
            # emit key-value pair: (word, (current sum, count)), `;` acts as a separator
            if current_word is not None:
                print(f"{current_word};{current_sum};{count}")

            current_word = word
            current_sum = num
            count = 1

    if current_word == word:
        # emit last key-value pair if needed
        print(f"{current_word};{current_sum};{count}")


if __name__ == "__main__":
    main()
