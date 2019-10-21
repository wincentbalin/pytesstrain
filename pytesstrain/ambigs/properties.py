"""
Ambiguities properties.
"""

import json
from collections import defaultdict


class AmbiguityProperties:
    def __init__(self, mandatory: bool):
        self.mandatory = mandatory
        self.count = 0
        self.distribution = defaultdict(int)

    def add(self, value):
        self.count += 1
        self.distribution[value] += 1


class AmbiguityPropertiesJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AmbiguityProperties):
            return o.__dict__
        else:
            return json.JSONEncoder.default(o)


def dump_ambiguity_properties(ap: dict, fn: str):
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(sorted(ap.items(), key=lambda i: i[1].count, reverse=True), f,
                  ensure_ascii=False, indent=4, cls=AmbiguityPropertiesJSONEncoder)


def is_mandatory(err: str, words: list) -> bool:
    """
    This function checks whether a word containing the error string exists.
    :param err: error string
    :param words: list of words
    :return: whether the correction can be specified as mandatory
    """
    for word in words:
        if err in word:
            return False
    else:
        return True


def extract_ambiguities(ref: str, hyp: str) -> list:
    """
    This function extracts identifiable ambiguities. Only ambiguities within the equal amount of words
    in both reference and hypothesis are processed. Then the code tries to find boundaries of error string,
    as it subtracts common prefix and suffix of words. If length of both error and correction is > 7, it will not
    be loaded by Tesseract OCR (search for MAX_AMBIG_SIZE constant in Tesseract source code).
    :param ref: reference string
    :param hyp: hypothesis string
    :return: list of tuples, where each tuple contains error and correction
    """
    ref_words = ref.split()
    hyp_words = hyp.split()
    ambiguities = []
    if len(ref_words) == len(hyp_words):  # Equal amount of words means ambiguity(-ies) is within one word
        for rw, hw in zip(ref_words, hyp_words):
            if rw != hw:
                error = hw
                correction = rw
                # Remove common prefix
                while len(error) > 1 and len(correction) > 1 and error[0] == correction[0]:
                    error = error[1:]
                    correction = correction[1:]
                # Remove common suffix
                while len(error) > 1 and len(correction) > 1 and error[-1] == correction[-1]:
                    error = error[:-1]
                    correction = correction[:-1]
                # Store results
                ambiguities.append((error, correction))
    return ambiguities
