import nltk
import sys
import os
import string
import math
import pickle

FILE_MATCHES = 1
SENTENCE_MATCHES = 2

def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Load files & calculate IDF values across files
    files = load_files(sys.argv[1])

    # Computationally expensive part - Can be skipped if you determine the files
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF - We can skip this part if we only have one file
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Alternatively define the files yourself if e.g. only one
    # filenames = ["Marketing.txt"]


    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_dict = {}

    for file_name in os.listdir(directory):
        # Skip hidden files
        if file_name.startswith("."):
            continue
       
        with open(os.path.join(directory, file_name), "r") as txt_file:
            # Read contents into string & add to dict
            # data = txt_file.read()
            file_dict[file_name] = txt_file.read()
    
    return file_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Tokenize words & turn into lowercase
    words = nltk.word_tokenize(document.lower())

    # Define stopwords
    stopwords = set(nltk.corpus.stopwords.words("english"))

    # Making a shallow copy to prevent skipping when deleting values
    for word in words.copy():
        # Remove punctuation words
        if word in string.punctuation:
            words.remove(word)
        # Remove stop words such as "yourself", "ours"
        if word in stopwords:
            words.remove(word)

    return words

def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    # Turn values into set to save iterating on double words
    global_set = set()
    # IDF for a word = ln (Total No of Docs / Total No of appearances in Docs)
    idf_dict = {}

    # Global set with all unique words from all documents
    for key in documents:
        global_set = global_set | set(documents[key])

    # Iterating through individual sets
    for word in global_set:
        # initialize idf score to 0
        idf_dict[word] = 0
        for key in documents:
            if word in set(documents[key]):
                # Increment appearances
                idf_dict[word] += 1
        # Calc final idf score
        idf_dict[word] = math.log(len(documents)/idf_dict[word])
    return idf_dict

    # Improvement ideas:
    # Only initialize set(documents[key]) once
    # Try to combine the two for loops

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # Create dictionary for scoring files and initialize to 0
    file_scores = {}
    for file_name in files:
        file_scores[file_name] = 0

    # Iterate through words in query
    for word in query:

        # Get IDF score of that word
        if word in idfs:
            idf_score = idfs[word]
        else: 
            # If we don't have this word we can skip it since we also won't get any TF
            continue

        # Calculate TF * IDF Score of that word PER document & add for each document
        for key, values in files.items():
            file_scores[key] += idf_score * values.count(word)

    # Turn dictionary into list sorted by values:
    ranked = sorted(file_scores, key=lambda key: file_scores[key], reverse=True)
    
    return ranked[:n]
    


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # Similar looping to top_files:
    sentence_scores = {}
    for sentence in sentences:
        sentence_scores[sentence] = 0

    for word in query:
        if word in idfs:
            idf_score = idfs[word]
        else: 
            continue
        for sentence in sentences:
            if word in sentences[sentence]:
                sentence_scores[sentence] += idf_score
            

    # Sort by two keys: Query term density (2nd) and score (1st)
    # QTD: Words in query / Length of sentences
    def sort_qtd(key):
        count = 0
        for word in query:
            if word in sentences[key]:
                count += 1
        if count != 0:
            return count/len(sentences[key])
        else:
            return 0

    ranked_qtd = sorted(sentence_scores, key=sort_qtd, reverse=True)

    ranked_idf_qtd = sorted(ranked_qtd, key=lambda key: sentence_scores[key], reverse=True)

    return ranked_idf_qtd[:n]


if __name__ == "__main__":
    main()
