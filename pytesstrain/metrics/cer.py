from editdistance import distance


def cer(ref: str, hyp: str) -> float:
    """Calculate CER as in https://github.com/finos/greenkey-asrtoolkit/blob/master/asrtoolkit/wer.py"""
    return distance(ref, hyp) / len(ref)
