#!/usr/bin/env python3
"""
Create single-line ground truth files from source file or directory.
"""

import re
import sys
import logging
import argparse
from pathlib import Path
from typing import List, Any


RE_LINE_ENDING = re.compile('\r?\n')


def generate_gt_txt(source: Path, gt_dir: Path) -> List[str]:
    for line_number, line in enumerate(RE_LINE_ENDING.split(source.read_text(encoding='utf8')), 1):
        gt_txt = gt_dir / '{}.{:06d}.gt.txt'.format(source.name, line_number)
        gt_txt.write_text(line + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('source', help='Source file or directory with .txt files')
    parser.add_argument('gt_dir', help='Ground truth directory')
    args = parser.parse_args()

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)

    gt_txt_files = []  # type: List[str]
    source = Path(args.source)
    gt_dir = Path(args.gtdir)

    if source.is_dir():
        for path in source.rglob('*.txt'):
            gt_txt_files += generate_gt_txt(path, gt_dir)
    else:
        gt_txt_files += generate_gt_txt(source, gt_dir)


if __name__ == '__main__':
    main()
