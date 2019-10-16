#!/usr/bin/env python3
"""Run tests for specified language"""

import sys
import argparse


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('-d', '--fonts_dir', help='Directory with fonts')
    parser.add_argument('-f', '--fonts', help='Fonts separated by comma')
    parser.add_argument('-e', '--exposures', help='Exposures separated by comma')
    args = parser.parse_args()

    fonts = args.fonts.split(',')
    exposures = map(int, args.exposures.split(','))


if __name__ == '__main__':
    main()
