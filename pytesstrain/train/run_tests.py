"""Multiple tests (parallel) runner."""

from itertools import product
from concurrent.futures import ProcessPoolExecutor

from .run_test import run_test


def run_tests(lang: str, ref: str, wrap: int, fonts_dir: str, fonts: list, exposures: list, config=''):
    pass
