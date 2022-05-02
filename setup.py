from setuptools import setup, find_packages

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytesstrain',
    version='0.1.16',
    packages=find_packages(),
    url='https://github.com/wincentbalin/pytesstrain',
    license='Apache License (2.0)',
    author='Wincent Balin',
    author_email='wincent.balin+pytesstrain@gmail.com',
    description='Collection of utilities for Tesseract OCR training',
    install_requires=['pytesseract', 'editdistance'],
    keywords=['Tesseract', 'OCR', 'training'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={'console_scripts': [
        'create_dictdata = pytesstrain.cli.create_dictdata:main',
        'create_ground_truth = pytesstrain.cli.create_ground_truth:main',
        'rewrap = pytesstrain.cli.rewrap:main',
        'language_metrics = pytesstrain.cli.language_metrics:main',
        'collect_ambiguities = pytesstrain.cli.collect_ambiguities:main',
        'json2unicharambigs = pytesstrain.cli.json2unicharambigs:main'
    ]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Text Processing',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ]
)
