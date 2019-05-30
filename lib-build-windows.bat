@echo off
echo Download articles
python wiki_downloader.py
echo Create the tar.gz in bash! Enter following command
echo.
echo    tar czvf wiki-files/wikiLib.tar.gz wiki-files/unprocessed-lib/*
echo.
pause
echo.
echo Extracting articles
python utils\WikiExtractor.py -o wiki-files\ wiki-files\wikiLib.tar.gz
echo.
echo Splitting document
python doc_splitter.py
echo.
IF EXIST wiki.db echo Deleting old database
IF EXIST wiki.db DEL /F wiki.db
echo.
echo Building index
python build_inv_index.py
echo.
echo.
echo Done!
pause