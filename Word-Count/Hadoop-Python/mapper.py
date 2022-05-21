#!/usr/bin/env python3

import re
import sys


def main():
    for chunk in sys.stdin:
        # put the text into the lowercase and split it by words
        words = re.findall(r"[\w']+", chunk.lower())

        for word in words:
            # emit key-value pair: (word, 1), `;` acts as a separator
            print(f"{word};1")


if __name__ == "__main__":
    main()
