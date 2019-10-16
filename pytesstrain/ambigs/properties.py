"""
Ambiguities properties.
"""

import json


class AmbiguityProperties:
    def __init__(self, mandatory: bool):
        self.mandatory = mandatory
        self.count = 0
        self.distribution = {}

    def add(self, value):
        self.count += 1
        if value in self.distribution:
            self.distribution[value] += 1
        else:
            self.distribution[value] = 1


class AmbiguityPropertiesJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, AmbiguityProperties):
            return o.__dict__
        else:
            return json.JSONEncoder.default(o)

