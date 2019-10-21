"""Multiple tests (parallel) runner."""

from itertools import product
from concurrent.futures import ProcessPoolExecutor
from typing import List

from .run_test import run_test


def run_tests(lang: str, ref: str, wrap: int, fonts_dir: str, fonts: list, exposures: list, config='') -> List[tuple]:
    """
    Run run_test function on multiple processors simultaneously.
    Returns tuples (reference, hypothesis, font, exposure).
    """
    with ProcessPoolExecutor(max_workers=None) as executor:
        futures = [executor.submit(run_test, lang, ref, wrap, fonts_dir, font, exposure, config)
                   for font, exposure in product(fonts, exposures)]
    return [future.result() for future in futures]
