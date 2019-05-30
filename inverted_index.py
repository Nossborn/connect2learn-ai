#
#   Takes processed wiki documents and creates an inverted index database,
#   with one table that contains the docs path and a correlating integer id
#   and one table with all different words from all documents and an
#   associated coloum with the doc ids of the docs where those words exist
#	in. This way when we search for a query, it doesn't have to search for
#	it in docs we know don't contain it.
#

import glob
import io
import sqlite3
import sys

from os.path import join

from base import load_stopwords, stem, tokenize

def build_word_to_tf(path, stopwords=None):
    if stopwords is None:
        stopwords = set()
    
    word_to_tf = {}
    with io.open(path, encoding='utf-8', errors='ignore') as f:
        for word in tokenize(f.read()):
            word = stem(word)
            if word in stopwords:
                continue
            
            if word not in word_to_tf:
                word_to_tf[word] = 1
            else:
                word_to_tf[word] += 1
    return word_to_tf

def build_inverted_index(db_path, data_path, stopwords=None):
    # Setup db
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('CREATE TABLE if not exists docs (doc text, id integer)')
    c.execute('CREATE TABLE if not exists inv_index (term, docs, tfs)')
    conn.commit()
    
    vocabulary = set()
    files = glob.glob(join(data_path, '*'))
    for i, f in enumerate(files):
        f = f.replace("\\", "/")
        c.execute('INSERT INTO docs values(?,?)', (f, i))
        word_to_tf = build_word_to_tf(f, stopwords)
        print('%s %d/%d' % (f, i, len(files) - 1))
        new_words = []
        for word in word_to_tf:
            if word not in vocabulary:
                vocabulary.add(word)
                new_words.append((word, str(i), str(word_to_tf[word])))
            else:
                c.execute('UPDATE inv_index SET docs=docs||?, tfs=tfs||? WHERE term=?',
                          (',%d' %i, ',%d' %word_to_tf[word], word))
        c.executemany('INSERT INTO inv_index VALUES (?,?,?)', new_words)
        conn.commit()
    conn.close()