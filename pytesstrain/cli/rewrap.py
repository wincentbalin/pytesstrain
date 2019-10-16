#!/usr/bin/env python3
"""Rewrap lines without breaking words"""

import sys
import argparse
import textwrap


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('infile', type=argparse.FileType('r', encoding='UTF-8'), help='Input file')
    parser.add_argument('outfile', type=argparse.FileType('w', encoding='UTF-8'), help='Output file')
    parser.add_argument('width', type=int, help='Output line width')
    args = parser.parse_args()

    for line in args.infile:
        for wrapped in textwrap.wrap(line, args.width):
            args.outfile.write(wrapped + '\n')


if __name__ == '__main__':
    main()
