#!/usr/bin/env python3


import sys


def main():
    current_word = None
    current_count = 0
    word = None

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        word, count = key_value.split(';')
        count = int(count)

        if current_word == word:
            current_count += count
        else:
            # emit key-value pair: (word, count sum), `;` acts as a separator
            if current_word is not None:
                print(f"{current_word};{current_count}")

            current_word = word
            current_count = count

    if current_word == word:
        # emit last key-value pair if needed
        print(f"{current_word};{current_count}")


if __name__ == "__main__":
    main()
