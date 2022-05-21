#!/usr/bin/env python3

import re
import lorem
import argparse
import numpy as np
import pandas as pd
from functools import reduce


def compute_TF(word_dict, max_freq):
    tf_dict = dict()
    for word, count in word_dict.items():
        tf_dict[word] = count / float(max_freq)
    return tf_dict


def compute_IDF(word_dict_list):
    N = len(word_dict_list)

    idf_dict = dict.fromkeys(word_dict_list[0].keys(), 0)
    for chunk_dict in word_dict_list:
        for word, count in chunk_dict.items():
            if count > 0:
                idf_dict[word] += 1

    for word, count in idf_dict.items():
        idf_dict[word] = np.log2(N / count)

    return idf_dict


def compute_TFIDF(tf, idfs):
    tfidf_dict = dict()
    for word, val in tf.items():
        tfidf_dict[word] = val * idfs[word]
    return tfidf_dict


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-n', type=int, help="Number of chunks",
                        metavar='num', default=3)

    args = parser.parse_args()

    chunks = list()
    for i in range(args.n):
        chunks.append(re.findall(r"[\w']+", lorem.paragraph()))

    word_set = reduce(lambda ch1, ch2: set(ch1).union(set(ch2)), chunks)
    word_dict = [dict.fromkeys(word_set, 0) for _ in range(args.n)]

    max_freq = [0] * args.n

    for i in range(args.n):
        for word in chunks[i]:
            word_dict[i][word] += 1
            max_freq[i] = max(max_freq[i], word_dict[i][word])

    tfs = [compute_TF(word_dict[i], max_freq[i]) for i in range(args.n)]
    idfs = compute_IDF(word_dict)
    tf_idfs = [compute_TFIDF(tfs[i], idfs) for i in range(args.n)]

    tf_df = pd.DataFrame.from_records(tfs)
    idf_df = pd.DataFrame(idfs, index=[0])
    tf_idf_df = pd.DataFrame.from_records(tf_idfs)

    print("TF:")
    print(tf_df.T)
    print("\nIDF:")
    print(idf_df.T)
    print("\nTF-IDF:")
    print(tf_idf_df.T)


if __name__ == "__main__":
    main()
