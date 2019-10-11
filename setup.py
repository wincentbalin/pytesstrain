from setuptools import setup

setup(
    name='pytesstrain',
    version='0.1.0',
    packages=['pytesstrain'],
    url='https://github.com/wincentbalin/pytesstrain',
    license='Apache License (2.0)',
    author='Wincent Balin',
    author_email='wincent.balin@gmail.com',
    description='Collection of utilities for Tesseract OCR training',
    install_requires=['pytesseract', 'jiwer'],
    entry_points={'console_scripts': [
        'create_dictdata = pytesstrain.cli.create_dictdata:main',
        'rewrap = pytesstrain.cli.rewrap:main'
    ]}
)
