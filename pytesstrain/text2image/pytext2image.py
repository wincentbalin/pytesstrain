"""
This file is essentially a reimplementation of pytesseract, adjusted for text2image.
"""

import os
import sys
import shlex
import subprocess
import tempfile

from pytesseract.pytesseract import subprocess_args, timeout_manager, get_errors, TesseractError


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
                   fonts_dir,
                   font,
                   exposure,
                   config='',
                   nice=0,
                   timeout=0):
    cmd_args = []

    if not sys.platform.startswith('win32') and nice != 0:
        cmd_args += ('nice', '-n', str(nice))

    cmd_args += (text2image_cmd, '--text', input_filename, '--outputbase', output_filename_base)
    cmd_args += ('--fonts_dir', fonts_dir, '--font', font, '--exposure', str(exposure))

    if config:
        cmd_args += shlex.split(config)

    try:
        proc = subprocess.Popen(cmd_args, **subprocess_args())
    except OSError:
        raise Text2imageNotFoundError()

    with timeout_manager(proc, timeout) as error_string:
        if proc.returncode:
            raise Text2imageError(proc.returncode, get_errors(error_string))


def run_and_get_output(textlines,
                       fonts_dir,
                       font,
                       exposure=0,
                       nice=0,
                       timeout=0):
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', suffix='.txt', delete=False) as tf:
        tf.writelines([line + '\n' for line in textlines])
        txtfn = tf.name
        basefn, _ = os.path.splitext(txtfn)
        imgfn = basefn + '.tif'
        boxfn = basefn + '.box'

    run_text2image(txtfn, basefn, fonts_dir, font, exposure, nice, timeout)

    return basefn, txtfn, imgfn, boxfn
