#!/usr/bin/env python3


import sys


def main():
    current_word = None
    current_sum = 0
    count = 1
    word = None

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        word, num = key_value.split(';')
        num = int(num)

        if current_word == word:
            current_sum += num
            count += 1
        else:
            # emit key-value pair: (word, mean), `;` acts as a separator
            if current_word is not None:
                print(f"{current_word};{current_sum / count:.4}")

            current_word = word
            current_sum = num
            count = 1

    if current_word == word:
        # emit last key-value pair if needed
        print(f"{current_word};{current_sum / count:.4}")


if __name__ == "__main__":
    main()
