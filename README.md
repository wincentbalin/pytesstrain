# Python utilities for Tesseract OCR training

This module is a collection of different training utilities for [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).
These utilities are also implemented as console scripts, hence they can be run from command line. 

## Utilities

All utilities list their command line switches when run with the switch `--help`.

* `rewrap` just rewraps text lines by specified maximal line length
* `create_dictdata` creates all word- and n-gram-lists from a text file, which are translated to DAWGs and added to the traineddata file then
* `language_metrics` creates random texts from supplied wordlist and tests for recognition error rates
* `collect_ambiguities` extracts error-correction pairs from reference-hypothesis pairs and stores them in a JSON file
* `json2unicharambigs` stores specified error-correction pairs from JSON file in a unicharambigs file


## Requirements

This module requires the following modules to work:

* pytesseract (Running Tesseract OCR)
* editdistance (Calculation of error rates)

## Packages

The module is split in several packages. The package `pytesstrain.train` contains the workhorse function
`run_text()`. The package `pytesstrain.cli` contains the utilities you might run at the command line. The package
`pytesstrain.ambigs` contains function around `unicharambigs` file. The package `pytesstrain.text2image` contains
the interface to the `text2image` command from the Tesseract OCR; the interface relies on `pytesseract` module
and is modelled after it as well. The package `pytesstrain.metrics` contains error rate calculations, as well
the interface class `Metrics`. The package `pytesstrain.utils` contains auxiliary functions.
