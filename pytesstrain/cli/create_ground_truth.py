#!/usr/bin/env python3
"""
Create single-line ground truth files from source file or directory.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List

RE_LINE_ENDING = re.compile('\r?\n')


def generate_gt_txt(source: Path, gt_dir: Path) -> List[Path]:
    gt_txt = []
    for line_number, line in enumerate(RE_LINE_ENDING.split(source.read_text(encoding='utf8')), 1):
        tidy_line = line.rstrip()
        if not tidy_line:  # Get rid of empty lines
            continue
        gt_txt = gt_dir / '{}.{:06d}.gt.txt'.format(source.stem, line_number)
        gt_txt.write_text(tidy_line + '\n', encoding='utf-8')
        gt_txt.append(gt_txt)
    return gt_txt


def main():
    parser = argparse.ArgumentParser(description=sys.modules[__name__].__doc__)
    parser.add_argument('source', help='Source file or directory with .txt files')
    parser.add_argument('gt_dir', help='Ground truth directory')
    args = parser.parse_args()

    source = Path(args.source)
    gt_dir = Path(args.gt_dir)

    gt_txt = []
    if source.is_dir():
        for path in source.rglob('*.txt'):
            gt_txt += generate_gt_txt(path, gt_dir)
    else:
        gt_txt += generate_gt_txt(source, gt_dir)


if __name__ == '__main__':
    main()
