# QA Module with Snap!

A simple factoid question-answering application for [Snap!](https://snap.berkeley.edu/).  
Developed for Ericsson's [Digital Lab AI course](https://www.ericsson.com/en/blog/2019/4/connect-to-learn-interns-develop-ai-course).

## Prerequisites

- Python 3.6
- [NumPy](http://www.numpy.org/)
- [NLTK](https://www.nltk.org/)
- [Pyttsx3](https://github.com/nateshmbhat/pyttsx3)
- Speech engine [[espeak](http://espeak.sourceforge.net/) or [pywin32](https://pypi.org/project/pywin32/)]
- [Google Chrome](https://www.google.com/chrome/) or [Mozilla Firefox](https://www.mozilla.org/en-US/firefox/new/)

## Usage

Windows:  
Open _START_Windows.bat

Linux: 
```bash
bash _START_Linux.sh
```

## Overview of AI module

This module implements a simple factoid question-answering (QA) system, loosely
based on [Lin, 2007]. Factoid QA systems attempt to answer factual questions
such as "what is X", "who is X", and "where is X". Modern implementations tend
to use named entity recognition (NER), relation extraction (RE), and dependency
parsing. Most state-of-the-art systems also employ deep learning models trained
on millions of manually labelled text snippets. We will however restrict
ourselves only to surface patterns, part-of-speech (POS) tagging, and some basic
statistical correlations, and use a purely unsupervised approach that doesn't
require any training. Unlike [Lin, 2007] we will only use Wikipedia XML dump as
information source, and rely on information redundancy within the documents
themselves.

The system can be broken down into a number of components:

* Formulate Query - reformulate the question into a query, based on rules
  (surface patterns and POS tags).
* Fetch Documents - convert query to n-grams, then fetch documents using
  inverted index and TF-IDF values
* Extract Exact Candidates - use the query as a regex pattern and apply it on
  retrieved documents
* Extract Inexact Candidates - treat the query as a bag-of-words (BoW) and
  perform a similarity comparison against each sentence in the retrieved
  documents
* Filter Candidates - using a set of rules, select the top answer(s)



Based on paper:

* An Exploration of the Principles Underlying Redundancy-Based Factoid Question Answering, J. Lin, 2007
