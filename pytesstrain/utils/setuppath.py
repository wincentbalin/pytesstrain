import os
import shutil

from ..text2image import pytext2image
import pytesseract


def setup_tesseract_path(path: str):
    """
    Set the supplied path and check for Tesseract binary.
    We assume that all binaries also reside there.
    """
    text2image_cmd = pytext2image.text2image_cmd
    tesseract_cmd = pytesseract.pytesseract.tesseract_cmd
    tesseract_found_in_supplied_path = shutil.which(tesseract_cmd, path=path)
    if tesseract_found_in_supplied_path:
        pytext2image.text2image_cmd = path + os.sep + text2image_cmd
        pytesseract.pytesseract.tesseract_cmd = path + os.sep + tesseract_cmd
    else:
        raise FileNotFoundError('Could not find tesseract cmd in supplied path ' + path)
