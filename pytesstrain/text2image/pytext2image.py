"""
This file is essentially a reimplementation of pytesseract, adjusted for text2image.
"""

import os
import sys
import shlex
import subprocess
import tempfile

from pytesseract.pytesseract import subprocess_args, timeout_manager, get_errors, TesseractError, Image


# CHANGE THIS IF TEXT2IMAGE IS NOT IN YOUR PATH, OR IS NAMED DIFFERENTLY
text2image_cmd = 'text2image'


class Text2imageError(TesseractError):
    pass


class Text2imageNotFoundError(EnvironmentError):
    def __init__(self):
        super(Text2imageNotFoundError, self).__init__(
            text2image_cmd + " is not installed or it's not in your path"
        )


def run_text2image(input_filename,
                   output_filename_base,
                   extension,
                   lang,
                   config='',
                   nice=0,
                   timeout=0):
    cmd_args = []

    if not sys.platform.startswith('win32') and nice != 0:
        cmd_args += ('nice', '-n', str(nice))

    cmd_args += (text2image_cmd, input_filename, output_filename_base)

    if lang is not None:
        cmd_args += ('-l', lang)

    if config:
        cmd_args += shlex.split(config)

    if extension and extension not in {'box', 'osd', 'tsv'}:
        cmd_args.append(extension)

    try:
        proc = subprocess.Popen(cmd_args, **subprocess_args())
    except OSError:
        raise Text2imageNotFoundError()

    with timeout_manager(proc, timeout) as error_string:
        if proc.returncode:
            raise Text2imageError(proc.returncode, get_errors(error_string))


def run_and_get_output(text,
                       extension,
                       nice=0,
                       timeout=0):
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt') as tf:
        txtfn = tf.name
        basefn, _ = os.path.splitext(txtfn)
        imgfn = basefn + '.' + extension.lower()
        boxfn = basefn + '.box'

    return txtfn, imgfn, boxfn
