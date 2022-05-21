#!/usr/bin/env python3


import sys


def main():
    current_word_length = None
    current_count = 0
    word_length = None

    for key_value in sys.stdin:
        # remove leading and trailing whitespace
        key_value.strip()

        word_length, count = key_value.split(';')
        word_length = int(word_length)
        count = int(count)

        if current_word_length == word_length:
            current_count += count
        else:
            # emit key-value pair: (word length, count sum), `;` acts as a separator
            if current_word_length is not None:
                print(f"{current_word_length};{current_count}")

            current_word_length = word_length
            current_count = count

    if current_word_length == word_length:
        # emit last key-value pair if needed
        print(f"{current_word_length};{current_count}")


if __name__ == "__main__":
    main()
