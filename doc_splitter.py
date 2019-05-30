#
#	This takes a text document with processed wikipedia articles attached
#	end to end and splits it by article. It then saves these articles in
#	seperate files named after the article itself.
#	This is ran from the lib-build-windows/lib-build-linux file.
#

import io
import os

if os.name == 'windows':
	wiki_library = "wiki-files\\wiki-library\\"
	wiki_files = "wiki-files\\AA\\wiki_00"
else:
	wiki_library = "wiki-files/wiki-library/"
	wiki_files = "wiki-files/AA/wiki_00"


def main():
	with io.open(wiki_files, 'r', encoding='utf8') as input_file:
		articles = input_file.read().split('</doc>')
		articles.pop() #Last in list seems to be empty? removing it for now 
	print("Articles loaded!")
	
	for article in articles:
		article_name = ((article.split('title="')[1]).split('">')[0]).replace(' ', '-')
		with io.open(wiki_library + article_name, 'w+', encoding='utf8') as output_file:
			output_file.write(article)
			print(" - Creating " + article_name + " file...")


if __name__ == '__main__':
	main()