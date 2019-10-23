from collections import defaultdict
from statistics import median
from typing import Dict, List, Union

from .wer import wer
from .cer import cer


class Metrics:
    """
    Metrics calculator.
    """
    def __init__(self):
        self.values = defaultdict(list)
        self.active = {'wer': False, 'cer': False}
        self.metrics = {'wer': wer, 'cer': cer}
        self.labels = {'wer': 'WER', 'cer': 'CER'}

    def activate(self, name: Union[str, List[str]]):
        if type(name) == str and name in self.active:
            self.active[name] = True
        elif type(name) == list:
            for nm in name:
                if nm in self.active:
                    self.active[nm] = True
        else:
            raise ValueError('Something wrong with the metric name')

    def add_pair(self, ref: str, hyp: str):
        for name, active in self.active.items():
            if active:
                self.values[name].append(self.metrics[name](ref, hyp))

    def get_results(self) -> Dict[str, float]:
        """
        Calculate median results from accumulated metrics.
        :return: Dictionary with label, value of every active metric
        """
        return {self.labels[name]: median(self.values[name]) for name, active in self.active.items() if active}
