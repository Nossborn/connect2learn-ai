#	
#	A file to test the qa_controller and qa. Here you can type
#	questions/queries directly in the terminal. Should give an identical
#	result to what it would give if the request came from the server/snap.
#	Usage in terminal like below ([] means optional parameter, / means or):
#
#	python qa-test.py --question "Question here" [--usebigrams] [--overlap-only / --cosine-only / --exact-only] [--normalize] [--num-inexact-matches]
#	
#	example:
#	python qa-test.py --question "Who is wonder woman" --overlap-only --normalize --numexact matches 2
#

import argparse
import sys
import time

from qa import reformulate_query
from qa_controller import answer_q
from qa_controller import retrieve_inexact_matches
from qa_controller import retrieve_exact_matches

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--use-bigrams', dest='use_bigrams',
                        action='store_true',
                        help='Use bigrams for inexact matching')
    parser.add_argument('--exact-only', dest='exact_matches_only',
                        action='store_true',
                        help='Apply only exact regex matching')
    parser.add_argument('--overlap-only', dest='inexact_matches_overlap_only',
                        action='store_true',
                        help='Apply only the "bag of words" matching')
    parser.add_argument('--cosine-only', dest='inexact_matches_cosine_only',
                        action='store_true',
                        help='Apply only the "bag of words" matching')
    parser.add_argument('--case-sensitive', dest='case_sensitive',
                        action='store_true',
                        help='Use case-sensitive regex matching')
    parser.add_argument('--normalize', dest='normalize', action='store_true',
                        help='''Log-normalize query and sentence length when
                                performing inexact matching''')
    parser.add_argument('--no-stopwords', dest='no_stopwords',
                        action='store_true',
                        help='Use case-sensitive regex matching')
    parser.add_argument('--num-inexact-matches', dest='num_inexact_matches',
                        type=int, default=1, help='''Number of inexact matches 
                        to return (1..3)''')
    parser.add_argument('--question', help='Question (please use quotes)')
    
    parser.set_defaults(case_sensitive=False)
    parser.set_defaults(exact_matches_only=False)
    parser.set_defaults(inexact_matches_overlap_only=False)
    parser.set_defaults(inexact_matches_cosine_only=False)
    parser.set_defaults(normalize=False)
    parser.set_defaults(no_stopwords=False)
    parser.set_defaults(use_bigrams=False)
    args = parser.parse_args()

    if not args.question:
        parser.print_help()
        sys.exit(1)
    
    if args.num_inexact_matches < 1 or args.num_inexact_matches > 3:
        parser.print_help()
        sys.exit(1)
    
    start = time.time()
    if(args.inexact_matches_overlap_only):
        query = reformulate_query(args.question)[1]
        retrieve_inexact_matches(query, args.normalize, args.num_inexact_matches, "overlap", use_bigrams=args.use_bigrams)
    
    elif(args.inexact_matches_cosine_only):
        query = reformulate_query(args.question)[1]
        retrieve_inexact_matches(query, args.normalize, args.num_inexact_matches, "cosine", use_bigrams=args.use_bigrams)
    
    elif(args.exact_matches_only):
        query = reformulate_query(args.question)[1] #Without the regex pattern, it is added later
        retrieve_exact_matches(query)
    
    else:
        answer_q(args.question, args.case_sensitive, args.exact_matches_only, args.normalize, args.num_inexact_matches, args.no_stopwords, args.use_bigrams)
    
    end = time.time()
    print(str(round(end - start, 6)) + "s runtime")
    

if __name__ == "__main__":
    main()

