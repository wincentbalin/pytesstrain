"""
Single test runner.
"""

import os
import textwrap

from ..tesseract import run_and_get_output as run_tesseract
from ..text2image import run_and_get_output as run_text2image


def run_test(lang: str, ref: str, wrap: int, fonts_dir: str, font: str, exposure: int, config=''):
    # Create test image
    basefn, txtfn, imgfn, boxfn = run_text2image(textwrap.wrap(ref, wrap), fonts_dir, font, exposure)
    os.remove(txtfn)
    os.remove(boxfn)
    # OCR test image
    hyp = run_tesseract(imgfn, 'txt', lang, config=config)
    os.remove(imgfn)
    return ref, hyp, font, exposure
