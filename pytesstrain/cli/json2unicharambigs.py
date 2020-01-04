#!/usr/bin/env python3
"""
Convert collected ambiguities from JSON file to unicharambigs file.
"""

import sys
import json
import argparse

MAX_LENGTH_SAFE = 10 - len(' ') - len(' 1')


def check_standard(err: str, corr: str) -> bool:
    return len(err) + len(corr) <= MAX_LENGTH_SAFE


def check_safe(err: str, corr: str) -> bool:
    return len(err) <= 3 and len(corr) <= 3


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--mode', choices=['standard', 'safe'], help='Length checking mode', default='safe')
    parser.add_argument('-e', '--min_entries', type=int, help='Minimal amount of entries in distribution', default=0)
    parser.add_argument('-o', '--mandatory_only', action='store_true', help='Store only mandatory ambiguities')
    parser.add_argument('json', type=argparse.FileType('r', encoding='utf-8'), help='JSON file with collected ambiguities')
    parser.add_argument('unicharambigs', help='Unicharambigs file (format v2)')
    args = parser.parse_args()

    collected = json.load(args.json)
    ambiguities = []
    for prop in collected:
        key = prop[0]
        err, corr = key[0], key[1]
        if args.mode == 'safe' and not check_safe(err, corr):
            continue
        elif args.mode == 'standard' and not check_standard(err, corr):
            continue
        entries = prop[1]
        mandatory = entries['mandatory']
        if args.mandatory_only and not mandatory:
            continue
        if len(entries['distribution']) < args.min_entries:
            continue
        ambiguities.append((err, corr, '1' if mandatory else '0'))

    if len(ambiguities) == 0:
        sys.exit('No ambiguities match provided parameters')

    with open(args.unicharambigs, 'w', encoding='utf-8', newline='\n') as uf:
        print('v2', file=uf)
        for ambiguity in ambiguities:
            print('{} {} {}'.format(*ambiguity), file=uf)


if __name__ == '__main__':
    main()
