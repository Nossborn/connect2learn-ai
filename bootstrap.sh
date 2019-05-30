#!/bin/bash

export PYTHON_USER_BIN=$(python -c 'import site; print site.USER_BASE + "/bin"')
export PATH=$PYTHON_USER_BIN:$PATH

pip install --user nltk
python -c 'import nltk; nltk.download("punkt");'
python -c 'import nltk; nltk.download("averaged_perceptron_tagger")'