import random


def create_word_sequence(words: list, length=10) -> str:
    """
    Create string of random words (useful for testing).
    :param words: list of words
    :param length: amount of words
    :return: string of random words
    """
    return ' '.join(random.sample(words, length))
