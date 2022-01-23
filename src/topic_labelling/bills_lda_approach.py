from inspect import CORO_CLOSED
import nltk
import re
from vote_data_parser_copy import get_all_bill_text
from nltk.stem.snowball import SnowballStemmer

# not using this stuff anymore

from nltk.corpus import stopwords as sw
stopwords = sw.words('english')

# DATA CLEANING - could be useful to add words that appear in multiple classifications to our stopword list
common_words = ["bill", "national", "act", "program", "programs", "amends", "amend", "veterans", "code",
 "within", "shall", "federal", "sets", "may", "year", "united", "states", "american"]
for word in common_words:
    stopwords.append(word)

# corpus = complete set of documents (so list of all bill summaries - which will be themselves lists of strings)
corpus = []

billTextList = get_all_bill_text()

for billText in billTextList:
    corpus.append(billText.desc)

from os import listdir
from os.path import isfile, join

def get_data():
    data_path = "long_term_bill_records/summary"
    filenameList = [f for f in listdir(data_path) if isfile(join(data_path, f))]
    for filename in filenameList:
        file = open(f"{data_path}/{filename}", "r")
        desc = file.readline()
        corpus.append(desc)

# used to remove non-alphabetical characters and lowercase words
def tokenise(text):
    regex = re.compile('[^a-zA-Z]')
    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            clean_word = regex.sub('', word)
            if len(clean_word) > 1:
                tokens.append(clean_word.lower())
    return tokens

# stem the words to get them to their most general form
def stem(word):
    stemmer = SnowballStemmer("english")
    return stemmer.stem(word).strip()

def print_results():
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(max_df=0.8, max_features=10000,
                                    min_df=0.05, stop_words=stopwords,
                                    use_idf=True, tokenizer=tokenise,
                                    lowercase=True, preprocessor=stem)

    tfidf_matrix = tfidf_vectorizer.fit_transform(corpus)

    from sklearn.decomposition import LatentDirichletAllocation

    lda = LatentDirichletAllocation(n_components=11, random_state=42)
    lda.fit(tfidf_matrix)
    
    for i,topic in enumerate(lda.components_):
        print(f'Topic #{i}:')
        print([tfidf_vectorizer.get_feature_names_out()[i] for i in topic.argsort()[-10:]])
        print('\n')

#get_data()
print_results()