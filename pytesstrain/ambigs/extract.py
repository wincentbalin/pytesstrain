def extract(ref: str, hyp: str) -> list:
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
