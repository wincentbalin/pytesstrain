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


def dump_properties(ap: dict, fn: str):
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
