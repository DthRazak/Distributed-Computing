#!/usr/bin/env python3


import sys


def main():
    current_word = None
    word = None
    current_sum = 0
    current_count = 0

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        word, num, count = key_value.split(';')
        num, count = int(num), int(count)

        if current_word == word:
            current_sum += num
            current_count += count
        else:
            # emit key-value pair: (word, mean), `;` acts as a separator
            if current_word is not None:
                print(f"{current_word};{current_sum / current_count:.4}")

            current_word = word
            current_sum = num
            current_count = count

    if current_word == word:
        # emit last key-value pair if needed
        print(f"{current_word};{current_sum / current_count:.4}")


if __name__ == "__main__":
    main()
