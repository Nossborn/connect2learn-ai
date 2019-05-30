#
#	Downloads articles linked in wiki_list.txt under wiki-files. Then saves
#	these articles as seperate files in the folder unprocessed-lib.
#	This is ran from the lib-build-windows/lib-build-linux file.
#

import requests
import sys
import os

if os.name == "windows":
	unprocessed_lib_path = "wiki-files\\unprocessed-lib\\"
	wiki_list_path = "wiki-files\\wiki_list.txt"
else:
	unprocessed_lib_path = "wiki-files/unprocessed-lib/"
	wiki_list_path = "wiki-files/wiki_list.txt"


def download(filename, url):
	r = requests.get(url, allow_redirects=True)
	output_file = open(unprocessed_lib_path + filename, 'wb+')
	output_file.write(r.content)


def retrieve_list():
	try:
		text_file = open(wiki_list_path, 'r')
	except:
		print("Wiki list load in FAILED: please create wiki_list.txt file")
		sys.exit(0)

	wiki_list = []
	for line in text_file:
		if(line[-1] == '\n'):
			line = line[:-1]
		wiki_list.append(line)
	
	return wiki_list

def main():
	list = retrieve_list()
	print("Articles downloaded:")
	for link in list:
		name = link.split('/wiki/')[1]
		link = link.split('/wiki/')[0] + "/wiki/Special:Export/" + name
		download(name, link)
		print(" - " + name)
		print(link)


if __name__ == '__main__':
	main()