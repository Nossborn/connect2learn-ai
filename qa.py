import io
import math
import os
import re
import sqlite3
import sys

from base import argsort
from base import bigrams
from base import dot
from base import get_max_indexes
from base import idf
from base import load_stopwords
from base import pos_tag
from base import sent_tokenize
from base import stem
from base import str_to_int_vect
from base import tfidf
from base import tokenize

def cosine_similarity(vect1, vect2, use_bigrams=False):
    vocabulary = set(vect1 + vect2)

    if use_bigrams:
        vocabulary.update(bigrams(vect1) + bigrams(vect2))
    
    word_to_ix = {word: ix for ix, word in enumerate(vocabulary)}
    v1 = len(word_to_ix) * [0]
    v2 = len(word_to_ix) * [0]
    
    for word in vect1:
        v1[word_to_ix[word]] += 1
    
    for word in vect2:
        v2[word_to_ix[word]] += 1
    
    return dot(v1, v2) / float(math.sqrt(dot(v1, v1)) * math.sqrt(dot(v2, v2)))

def extract_exact_matches(doc, query, case_sensitive=False):
    """Apply regex `query` on `doc`; `flags` controls case sensitivity."""
    flags = re.IGNORECASE
    if case_sensitive:
        flags = 0
    
    selected = []
    for sent in doc:
        if re.match(query, sent, flags) is not None:
            selected.append(sent)
    return selected

def extract_inexact_matches(doc, query, match_type, normalize=False, k=3, use_bigrams=False):
    scores = []
    query = tokenize(query.lower())
    if(match_type=="overlap"):
        for sent in doc:
            scores.append(overlap_similarity(tokenize(sent.lower()), query, normalize, use_bigrams))
    if(match_type=="cosine"):
        for sent in doc:
            scores.append(cosine_similarity(tokenize(sent.lower()), query, use_bigrams))

    indexes = list(reversed(argsort(scores)))[:k]
    return [doc[i] for i in indexes]

def extract_passages(s, docs):
    """Return a list of strings containing at least one query term from `s`."""
    if os.name == 'windows':
        docs = [doc.replace('/', '\\') for doc in docs]
    
    query_terms = set(tokenize(s))
    passages = []
    for doc in docs:
        with io.open(doc, encoding='utf-8', errors='ignore') as f:
            for para in f:
                for sent in sent_tokenize(para):
                    if len(query_terms.intersection(set(tokenize(sent)))) == 0:
                        continue
                    passages.append(sent)
    return passages

def overlap_similarity(vect1, vect2, normalize=False, use_bigrams=False):
    """Return the length of overlap between two vectors."""
    overlap = len(set(vect1).intersection(set(vect2)))

    if use_bigrams:
        overlap += len(set(bigrams(vect1)).intersection(set(bigrams(vect2))))

    if not normalize:
        return overlap
    
    if overlap == 0:
        return 0
    
    return overlap / (math.log10(len(vect1)) + math.log10(len(vect2)))


def reformulate_query(s):
    """Turn a question `s` into a tuple of exact query and inexact query. Exact
    query is a regex and inexact query will serve as bag-of-words query. We use
    POS tagging to help with reformulating the query."""
    words = tokenize(s)
    tags = [tag for _, tag in pos_tag(words)]

    if tags[-1] == '.':
        words.pop()

    # what/who questions
    if tags[0] in set(['WP', 'WDT']):
        if tags[1] in set(['VBZ', 'VBD', 'VBP']):
            if tags[-1] is not 'IN':
                exact_query = '{0}\s*{1}\s*{2}'.format(' '.join(words[2:]),
                                                       '(?:\(.*\))?', words[1])
                inexact_query = '{0} {1}'.format(' '.join(words[2:]), words[1])
                return exact_query, inexact_query
    return s, s


def retrieve_documents(s, db):
    """Return list of doc paths given a string query `s` and database `db`. 
    Return `None` if no matches found.
    """
    terms = ['"%s"' %stem(term) for term in tokenize(s)]
    
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('''SELECT docs, tfs FROM inv_index 
                 WHERE term IN (%s)''' %(','.join(terms)))
    res = c.fetchall()

    if not res:
        return None
    
    # if only one result, get the doc(s) with highest tf
    if len(res) == 1:
        doc_ids = str_to_int_vect(res[0][0])
        tfs = str_to_int_vect(res[0][1])
        doc_ids = [doc_ids[i] for i in get_max_indexes(tfs)]
    else:
        # multiple results, get the intersection of doc ids
        sets = [set(str_to_int_vect(d)) for d, _ in res]
        doc_ids = list(set.intersection(*sets))

        # if no intersection, then return the documents with highest tf-idf
        if len(doc_ids) == 0:
            c.execute('SELECT id FROM docs')
            n = len(c.fetchall())
            for d, t in res:
                tf_idf = tfidf(n, len(str_to_int_vect(d)), str_to_int_vect(t))
                doc_ids += get_max_indexes(tf_idf)
    
    doc_ids = [str(i) for i in doc_ids]
    c.execute('''SELECT doc FROM docs WHERE id IN (%s)''' %(','.join(doc_ids)))
    return [res[0] for res in c.fetchall()]