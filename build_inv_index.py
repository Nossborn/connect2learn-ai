#
#	Calls the inverted_index and tells it where the database and stopwords
#	are and where wiki are.
#	This probably doesn't need to be a seperate file....
#

from base import load_stopwords
from inverted_index import build_inverted_index

stopwords = load_stopwords('stopwords.txt')
build_inverted_index('wiki.db', 'wiki-files/wiki-library/', stopwords)
