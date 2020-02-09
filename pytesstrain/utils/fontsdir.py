"""
Functions around fonts directory.
"""

import os
import platform


def default_fonts_dir() -> str:
    system = platform.system()
    if system == 'Windows':
        return os.path.join(os.environ['WINDIR'], 'Fonts')
    elif system == 'Linux':
        return '/usr/share/fonts'
    elif system == 'Darwin':
        return '/Library/Fonts'
    else:
        raise NotImplementedError('Unknown OS')
