# Python utilities for Tesseract OCR training

This module is a collection of different training utilities for [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
These utilities are also implemented as console scripts, hence they can be run from command line.

## Packages

The module is split in several packages. The package `pytesstrain.train` contains the workhorse function
`run_text()`. The package `pytesstrain.cli` contains the tolls you might run at the command line. The package
`pytesstrain.ambigs` contains function around `unicharambigs` file.

