from typing import List, Tuple
from editdistance import distance


def _prepare(s1: str, s2: str) -> Tuple[List[int]]:
    s1_words = s1.split()
    s2_words = s2.split()
    enum_words = {word: num for num, word in enumerate(set(s1_words + s2_words))}
    return [enum_words[word] for word in s1_words], [enum_words[word] for word in s2_words]


def wer(ref: str, hyp: str) -> float:
    """Calculate word error rate through converting words to integers."""
    ref_int, hyp_int = _prepare(ref, hyp)
    return distance(ref_int, hyp_int) / len(ref_int)
