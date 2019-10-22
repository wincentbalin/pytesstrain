#!/usr/bin/env python3
"""Run WER tests for specified language"""

import sys
import logging
import argparse
import statistics

from jiwer import wer

from pytesstrain.train import run_tests
from pytesstrain.utils import setup_tesseract_path, load_wordlist, create_word_sequence


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('-l', '--language', help='Language to test', required=True)
    parser.add_argument('-w', '--wordlist', help='Wordlist file', required=True)
    parser.add_argument('-i', '--iterations', type=int, help='Iterations to run', default=100)
    parser.add_argument('-p', '--path', help='Directory with Tesseract binaries')
    parser.add_argument('-a', '--wrap', help='Wrap line by amount of characters', type=int, default=70)
    parser.add_argument('-t', '--tessdata_dir', help='Tessdata directory')
    parser.add_argument('-d', '--fonts_dir', help='Directory with fonts')
    parser.add_argument('-f', '--fonts', help='Fonts separated by comma', required=True)
    parser.add_argument('-e', '--exposures', help='Exposures separated by comma', default='0')
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)

    if args.path:
        setup_tesseract_path(args.path)

    wordlist = load_wordlist(args.wordlist)
    fonts = args.fonts.split(',')
    exposures = list(map(int, args.exposures.split(',')))
    # Replacing backslashes is a workaround for pytesseract, as shlex.split therein swallows them
    # Look at https://github.com/jrnl-org/jrnl/issues/348#issuecomment-98616332 , the solution is there
    config = '--tessdata-dir ' + args.tessdata_dir.replace('\\', '/') if args.tessdata_dir else ''

    wer_list = []
    for iteration in range(1, args.iterations+1):
        logging.info('Iteration #{}'.format(iteration))
        ref = create_word_sequence(wordlist, 10)
        logging.info('REF: ' + ref)
        results = run_tests(args.language, ref, args.wrap, args.fonts_dir, fonts, exposures, config)
        hyp_list = [hyp for _, hyp, _, _ in results]
        ref_list = [ref] * len(hyp_list)
        value = wer(ref_list, hyp_list)
        wer_list.push(value)
        logging.info('WER: {}'.format(value))
    logging.info('Median WER: {}'.format(statistics.median(wer_list)))


if __name__ == '__main__':
    main()
