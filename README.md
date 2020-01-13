# Python tools for Tesseract OCR training

Training tools for [Tesseract OCR](https://github.com/tesseract-ocr/tesseract).

## Installation

Install using pip:

```
pip install pytesstrain
```

This will also install Python packages `pytesseract` (used for running Tesseract)
and `editdistance` (used for calculation of error rates).

## Getting started

This package contains tools for specific problems:

### text2image is crashing ([issue #1781 @ Tesseract OCR](https://github.com/tesseract-ocr/tesseract/issues/1781))

The text2image tool crashes, if text lines are too long. As stated in the issue above,
rewrapping text lines to smaller length is the official workaround for this problem.
For example, to reduce line length to 35 characters at most, run

```bash
rewrap corpus.txt corpus-35.txt 35
```

### Creating dictionary data from corpus file

In case you do not have a dictionary file for the training language, you might want
to create one from the corpus file. To create dictionary file for the language _lang_, run

```bash
create_dictdata -l lang -i corpus.txt -d ./langdata/lang
```

This tool creates following files:

* lang.training_text (copy of the corpus file)
* lang.wordlist (dictionary)
* lang.word.bigrams (word bigrams)
* lang.training_text.bigram_freqs (character bigram frequencies)
* lang.training_text.unigram_freqs (character frequencies)

The file `lang.wordlist.freq` is usually created by training tools, such as `tesstrain.sh` and the likewise,
so there is no need to create it with `create_dictdata`.

### Language metrics

The tool `language_metrics` runs Tesseract OCR over images of random word sequences, which are created
out of the supplied wordlist, and calculates _median_ metrics (currently CER and WER) from the results.
It enables you to assess the quality of your `.traineddata` file.

To calculate metrics for the language _lang_ with fonts _Arial_ and _Courier_ using wordlist file _lang.wordlist_,
run
```bash
language_metrics -l lang -w lang.wordlist --fonts Arial,Courier
```

### Creating unicharambigs file

There are two tools in this package, which enable automatic creation of an unicharambigs file.

The first tool, `collect_ambiguities`, compares the recognised text with the reference text and
extracts smallest possible differences as error and correction pairs, and stores them sorted by
frequency of occurrence in a JSON file. You may look at the ambiguities by yourself before
converting them to `unicharambigs` file with the second tool.

The second tool, `json2unicharambigs`, takes the intermediate JSON file and puts the ambiguities
into the `unicharambigs` file. The resulting file has _v2_ format. You may limit the ambiguities,
which go into the `unicharambigs` file, with additional command-line switches.

To create the file `lang.unicharambigs` for the language _lang_ using wordlist file _lang.wordlist_,
run
```bash
collect_ambiguities -l lang -w lang.wordlist --fonts Arial,Courier -o ambigs.json
json2unicharambigs --mode safe --mandatory_only ambigs.json lang.unicharambigs
```

### Creating ground truth files

To help with training og Tesseract>=4, the tool `create_ground_truth` creates single-line ground truth files
either from an input file or from a directory with `.txt` files (the tool searches the latter ones recursively).

To create ground truth files from a directory `corpora` in the directory `ground-truth`, run
```bash
create_ground_truth corpora ground-truth
```

## API Reference

The main workhorse is the function `pytesstrain.train.run_test`. There is also a parallel version,
`pytesstrain.train.run_tests`, which uses a pool of threads to run the former function on multiple processors
simultaneously (using threads instead of processes for parallelisation is possible, because the `run_test`
function starts processes itself and is thus I/O-bound).

The subpackage `tesseract` simply imports the package `pytesseract`. The subpackage `text2image` imitates
the former one, but for the `text2image` tool instead of `tesseract`.

The subpackage `metrics` contains implementation of metrics, such as CER and WER. The subpackage `utils` has
often-used, miscellaneous functions and the subpackage `ambigs` contains ambiguity processing functions.

Finally, the subpackage `cli` contains the console scripts.

## License

Pytesstrain is released under [Apache License 2.0](LICENSE).
