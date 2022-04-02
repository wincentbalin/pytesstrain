#!/usr/bin/env python3
"""
Create single-line ground truth files from source file or directory.
"""

import re
import sys
import logging
import argparse
from pathlib import Path
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor
from multiprocessing import cpu_count

from pytesstrain.text2image import run_text2image, Text2imageNotFoundError, Text2imageError
from pytesstrain.utils import setup_tesseract_path, default_fonts_dir

RE_LINE_ENDING = re.compile('\r?\n')


def generate_gt_txt(source: Path, gt_dir: Path, fonts: List[Tuple]) -> List[Tuple]:
    logging.debug('Processing {}'.format(source))
    gt_txt_and_font = []
    for line_number, line in enumerate(RE_LINE_ENDING.split(source.read_text(encoding='utf8')), 1):
        tidy_line = line.rstrip()
        if not tidy_line:  # Get rid of empty lines
            continue
        for font, font_safe in fonts:
            gt_txt = gt_dir / '{}.{:06d}.{}.exp{}.gt.txt'.format(source.stem, line_number, font_safe, 0)
            if gt_txt.exists():
                logging.warning('Overwriting existing file: {}'.format(gt_txt))
            gt_txt.write_text(tidy_line + '\n', encoding='utf-8')
            gt_txt_and_font.append((gt_txt, font))
    return gt_txt_and_font


def generate_image(gt_txt: Path, fonts_dir: Path, font: str, width: int):
    outputbase = gt_txt.with_suffix('').with_suffix('')  # Remove .gt.txt
    logging.debug('Generating {}'.format(outputbase.name))
    config = '--strip_unrenderable_words --xsize {} --ysize 300 --leading 32 --margin 12'.format(width)
    try:
        run_text2image(str(gt_txt), str(outputbase), str(fonts_dir), font, exposure=0, config=config)
    except Text2imageNotFoundError:
        logging.error('Could not find text2image')
    except Text2imageError as error:
        logging.error('text2image: {message} (return code: {code})'.format(message=error.message, code=error.status))
    if not outputbase.with_suffix(outputbase.suffix + '.tif').exists():  # Ensure that only renderable .gt.txt exist
        logging.warning('File {} is unrenderable! Removing it...'.format(gt_txt))
        gt_txt.unlink()
    outputbase.with_suffix(outputbase.suffix + '.box').unlink()


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('-p', '--path', help='Directory with Tesseract binaries')
    parser.add_argument('-d', '--fonts_dir', help='Directory with fonts', default=default_fonts_dir())
    parser.add_argument('-f', '--fonts', help='Fonts separated by comma', required=True)
    parser.add_argument('-w', '--width', help='Width of ground truth images', type=int, default=3600)
    parser.add_argument('source', help='Source file or directory with .txt files')
    parser.add_argument('gt_dir', help='Ground truth directory')
    args = parser.parse_args()

    if args.path:
        setup_tesseract_path(args.path)

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)

    fonts = [(font, font.replace(' ', '_')) for font in args.fonts.split(',')]
    fonts_dir = Path(args.fonts_dir)
    image_width = args.width
    source = Path(args.source)
    gt_dir = Path(args.gt_dir)

    logging.info('Processing .txt files')
    gt_txt_and_font = []
    if source.is_dir():
        for path in source.rglob('*.txt'):
            gt_txt_and_font += generate_gt_txt(path, gt_dir, fonts)
    else:
        gt_txt_and_font += generate_gt_txt(source, gt_dir, fonts)

    logging.info('Generating .tif files')
    with ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        for gt_txt, font in gt_txt_and_font:
            executor.submit(generate_image, gt_txt, fonts_dir, font, image_width)
    executor.shutdown(wait=True)
    logging.info('Done')


if __name__ == '__main__':
    main()
