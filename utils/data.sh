#!/bin/bash

DIR="${0%/*}"
wget -O $DIR/../enwiki.xml.bz2 https://dumps.wikimedia.org/enwiki/20190201/enwiki-20190201-pages-articles1.xml-p10p30302.bz2
mkdir -p $DIR/../wiki/
python $DIR/WikiExtractor.py -o $DIR/../wiki/ $DIR/../enwiki.xml.bz2
rm -rf $DIR/../enwiki.xml.bz2