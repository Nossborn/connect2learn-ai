#
#	This file is only here to test cosine and overlap similarity scores
#	based depending if you include bigrams or not. As of writing, enabling
#	bigrams has not impact at all for cosine.
#

from qa_controller import setup
from qa import cosine_similarity
from qa import overlap_similarity
from base import tokenize

def test(query, match_type):
	doc = setup(query, False)
	if(match_type=="cosine"):
		for sent in doc:
			score1=cosine_similarity(tokenize(sent.lower()), tokenize(query.lower()), True)
			score2=cosine_similarity(tokenize(sent.lower()), tokenize(query.lower()), False)

	if(match_type=="overlap"):
		for sent in doc:
			score1=overlap_similarity(tokenize(sent.lower()), tokenize(query.lower()), False, True)
			score2=overlap_similarity(tokenize(sent.lower()), tokenize(query.lower()), False, False)

	print("No Bigram: " + str(score2), "   |   Bigram: " + str(score1))
	if(score2 == score1):
		print("Exactly equal")

def s_score(query, match_type):
	doc = setup(query, False)
	#sent = "Two Three Four Five"
	sent = """One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections. The bedding was hardly able to cover it and seemed ready to slide off any moment. His many legs, pitifully thin compared with the size of the rest of him, waved about helplessly as he looked. "What's happened to me?" he thought. It wasn't a dream. His room, a proper human room although a little too small, lay peacefully between its four familiar walls. A collection of textile samples lay spread out on the table - Samsa was a travelling salesman - and above it there hung a picture that he had recently cut out of an illustrated magazine and housed in a nice, gilded frame. It showed a lady fitted out with a fur hat and fur boa who sat upright, raising a heavy fur muff that covered the whole of her lower arm towards the viewer. Gregor then turned to look out the window at the dull weather."""

	query = """Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts. Separated they live in Bookmarksgrove right at the coast of the Semantics, a large language ocean. A small river named Duden flows by their place and supplies it with the necessary regelialia. It is a paradisematic country, in which roasted parts of sentences fly into your mouth. Even the all-powerful Pointing has no control about the blind texts it is an almost unorthographic life One day however a small line of blind text by the name of Lorem Ipsum decided to leave for the far World of Grammar. The Big Oxmox advised her not to do so, because there were thousands of bad Commas, wild Question Marks and devious Semikoli, but the Little Blind Text didn’t listen. She packed her seven versalia, put her initial into the belt and made herself on the way. When she reached the first hills of the Italic Mountains, she had a last view back on the skyline of her hometown Bookmarksgrove, the headline of Alphabet Village and the subline of her own road, the Line Lane."""

	print(sent, "\n", query)
	if(match_type=="cosine"):
		score1=cosine_similarity(tokenize(sent.lower()), tokenize(query.lower()), True)
		score2=cosine_similarity(tokenize(sent.lower()), tokenize(query.lower()), False)

	if(match_type=="overlap"):
		score1=overlap_similarity(tokenize(sent.lower()), tokenize(query.lower()), False, True)
		score2=overlap_similarity(tokenize(sent.lower()), tokenize(query.lower()), False, False)

	print("No Bigram: " + str(score2), "   |   Bigram: " + str(score1))
	if(score2 == score1):
		print("Exactly equal")

test("wonder woman is", "cosine")