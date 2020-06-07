#!/usr/bin/env python3
"""
Create langdata directory from a corpus file.
"""

import argparse
import sys
import re
import string

from collections import Counter
from itertools import chain
from operator import itemgetter
from pathlib import Path
from shutil import copy2
from typing import List, Tuple, AnyStr

RE_PUNCTUATION = re.compile(r'[{}]'.format(string.punctuation))

def sorted_items(c: Counter) -> List[Tuple[AnyStr, int]]:
    """
    Sort list of items in Counter by their count, descending.
    :param c: Counter with items counted
    :return: Sorted list of items and their counts
    """
    return sorted(c.items(), key=itemgetter(1), reverse=True)


def wordlist_data(c: Counter) -> List[AnyStr]:
    """
    Extract items from counter to a list.
    :param c: Counter with items
    :return: Sorted list of Counter keys
    """
    return [word for word, _ in sorted_items(c)]


def freq_wordlist_data(c: Counter, threshold=0.95) -> List[Tuple[AnyStr, int]]:
    threshold_amount = int(sum(c.values()) * threshold)
    amount = 0
    freq_wordlist = []
    for item in sorted_items(c):
        freq_wordlist.append(item)
        amount += item[1]
        if amount > threshold_amount:
            break
    return freq_wordlist


def bigram_list_data(c: Counter) -> list:
    """
    Extract tuple keys from Counter to a list
    :param c: Counter with bigram keys
    :return: List of bigrams
    """
    return [item for item, _ in sorted_items(c)]


def one_column(ls: List[AnyStr]) -> str:
    """
    Join single list entries to a string.
    :param ls: List of strings
    :return: String separated by newlines
    """
    return '\n'.join(ls)


def two_columns(pairs: List[Tuple]) -> str:
    """
    Join pairs (or more) of strings to a string.
    :param pairs: List of tuples of strings
    :return: String separated by newlines
    """
    return '\n'.join([' '.join(map(str, t)) for t in pairs])


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('-d', '--directory', help='Output langdata directory')
    parser.add_argument('-i', '--input', help='Corpus file')
    parser.add_argument('-l', '--language', help='Language of the corpus (ISO 639-3)')
    parser.add_argument('--retain-punctuation', help='Do not remove punctuation in wordlists', action='store_true')
    args = parser.parse_args()

    word_count, word_bigram_count, bigram_count, unigrams_count = Counter(), Counter(), Counter(), Counter()
    with open(args.input, encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if not args.retain_punctuation:
            line = RE_PUNCTUATION.sub(' ', line)
        words = line.split()
        word_bigrams = [(words[i], words[i+1]) for i in range(len(words)-1)]
        bigrams = [word[i] + word[i+1] for word in words for i in range(len(word)-1) if len(word) > 1]
        unigrams = list(chain.from_iterable([list(word) for word in words]))

        word_count.update(words)
        word_bigram_count.update(word_bigrams)
        bigram_count.update(bigrams)
        unigrams_count.update(unigrams)

    od = Path(args.directory)
    of = od / args.language
    enc = 'utf-8'
    copy2(args.input, str(of.with_suffix('.training_text')))
    of.with_suffix('.wordlist').write_text(one_column(wordlist_data(word_count)), encoding=enc)
    of.with_suffix('.word.bigrams').write_text(two_columns(bigram_list_data(word_bigram_count)), encoding=enc)
    of.with_suffix('.training_text.bigram_freqs').write_text(two_columns(sorted_items(bigram_count)), encoding=enc)
    of.with_suffix('.training_text.unigram_freqs').write_text(two_columns(sorted_items(unigrams_count)), encoding=enc)


if __name__ == '__main__':
    main()
