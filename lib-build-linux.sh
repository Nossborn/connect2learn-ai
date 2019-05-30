#!/bin/bash
echo "Download articles"
python3 wiki_downloader.py
echo "
Tarring files..."
tar czvf "wiki-files/wikiLib.tar.gz" "wiki-files/unprocessed-lib/"
echo "
Extracting articles"
python3 ./utils/WikiExtractor.py -o wiki-files/ wiki-files/wikiLib.tar.gz
echo "
Splitting document"
python3 doc_splitter.py
if [ -f "wiki.db" ]; then
	echo "Deleting old database"
	rm wiki.db
fi
echo "Building index"
python3 build_inv_index.py
echo "

Done!"
exit