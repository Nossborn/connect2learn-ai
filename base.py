import math
import nltk

from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('english')

def argsort(v):
    """Return list of indexes from `v` sorted according to increasing values"""
    return sorted(range(len(v)), key=v.__getitem__)

def bigrams(words):
    return ['{0} {1}'.format(a, b) for a, b in zip(words[:-1], words[1:])]

def dot(u, v):
    """Return dot product of two vectors, assume equal length."""
    return sum([a * b for a, b in zip(u, v)])

def get_max_indexes(a):
    """Return a list of indexes in list `a` that have the highest value. If
    there is only one element that has the highest value, then only one index 
    will be returned.
    """
    m = max(a)
    return [i for i, val in enumerate(a) if val == m]

def idf(n, df):
    """Return a smoothed idf from `n` documents and `df` document frequency."""
    return math.log10((1 + n) / (1 + df)) + 1

def load_stopwords(path):
    """Load stop words from `path` and return a set."""
    stopwords = set()
    with open(path) as f:
        for line in f:
            stopwords.add(line.strip())
    return stopwords

def pos_tag(words):
    return nltk.pos_tag(words)

def sent_tokenize(s):
    return nltk.sent_tokenize(s)

def stem(w):
    return stemmer.stem(w)

def str_to_int_vect(s):
    """Convert a string `s` of comma-separated ints to a list of ints."""
    return [int(i) for i in s.split(',')]

def tfidf(n, df, v):
    """Return a vector of tf-idf values, applied on tf vector `v`, assuming doc 
    frequency `df` and num documents `n`.
    """
    i = idf(n, df)
    return [t * i for t in v]

def tokenize(s):
    return nltk.word_tokenize(s)