#   
#   This is where the query requests are handled. The query is 
#   

from qa import extract_exact_matches
from qa import extract_inexact_matches
from qa import extract_passages
from qa import reformulate_query
from qa import retrieve_documents

def setup(query, no_stopwords = False):
    #db_path = './wikiqa.db' OLD
    db_path = './wiki.db'
    if no_stopwords:
        db_path = './wikiqa_nostopwords.db' #Also old and never used
    
    docs = retrieve_documents(query, db_path)
    if docs is None:
        print('Sorry, no answer found :-(')
    return extract_passages(query, docs)

def answer_q(question, case_sensitive=False, exact_matches_only=False, normalize=False, num_inexact_matches=3, no_stopwords=False, use_bigrams=False):
    passages = setup(question, no_stopwords)

    exact_query, inexact_query = reformulate_query(question)
    print(exact_query)
    print(inexact_query)

    exact_matches = extract_exact_matches(passages, exact_query, 
                                          case_sensitive)
    if exact_matches:
        answer='\n'.join(exact_matches[:1])
        print(answer)
        return(answer)
    
    if not exact_matches_only:
        inexact_matches = extract_inexact_matches(passages, inexact_query, "overlap", normalize, num_inexact_matches, use_bigrams)
        if inexact_matches:
            answer='\n'.join(inexact_matches)
            print(answer)
            return(answer)
    
    answer = "No answer found" 
    print(answer)
    return answer

def retrieve_exact_matches(query, no_stopwords=False, case_sensitive=False):
    passages = setup(query, no_stopwords)
    #Replace last space with regex pattern \s*(?:\(.*\))?\s*
    # It is there so that the parenthesis in the retrieved sentence is ignored
    exact_query = query[::-1].replace(' ', r'\s*(?:\(.*\))?\s*'[::-1], 1)[::-1]
    print(exact_query)
    exact_matches = extract_exact_matches(passages, exact_query, 
                                                            case_sensitive)
    if exact_matches:
        answer='\n'.join(exact_matches[:1])
        print(answer)
        return(answer)

    answer = "No answer found" 
    print(answer)
    return answer

def retrieve_inexact_matches(query, normalize, num_inexact_matches, match_type, no_stopwords=False, use_bigrams=False):
    passages = setup(query, no_stopwords)
    inexact_query = query
    print(inexact_query)
    inexact_matches = extract_inexact_matches(passages, inexact_query, match_type, normalize, num_inexact_matches, use_bigrams)
    print(inexact_matches)
    if inexact_matches:
        answer='\n'.join(inexact_matches)
        print(answer)
        return(answer)

    answer = "No answer found" 
    print(answer)
    return answer