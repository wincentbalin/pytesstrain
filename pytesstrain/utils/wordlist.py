from typing import List


def load_wordlist(fn: str) -> List[str]:
    """
    Read specified wordlist.
    :param fn: Wordlist filename
    :return: List of words
    """
    with open(fn, encoding='utf-8') as f:
        return list(map(str.rstrip, f.readlines()))
