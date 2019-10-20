#!/usr/bin/env python3
"""Run WER tests for specified language"""

import sys
import argparse

from ..utils import create_word_sequence


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('-l', '--language', help='Language to test')
    parser.add_argument('-w', '--wordlist', help='Wordlist file')
    parser.add_argument('-i', '--iterations', type=int, help='Iterations to run', default=100)
    parser.add_argument('-d', '--fonts_dir', help='Directory with fonts')
    parser.add_argument('-f', '--fonts', help='Fonts separated by comma')
    parser.add_argument('-e', '--exposures', help='Exposures separated by comma')
    args = parser.parse_args()

    fonts = args.fonts.split(',')
    exposures = map(int, args.exposures.split(','))
    ref = create_word_sequence()


if __name__ == '__main__':
    main()
