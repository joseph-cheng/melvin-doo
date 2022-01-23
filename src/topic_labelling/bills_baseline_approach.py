# our pre-defined categories = {'oil', 'telecom', 'utilities', 'retail', 'health', 'real estate', 'precious metals', 'technology', 'finance', 'industrial', 'energy', 'materials'}
import re
import nltk
from vote_data_parser_copy import get_all_bill_text, Bill
#import textacy
#import textacy.ke
import pandas as pd
import nltk
#import spacy
#from tqdm import tqd

predefined_categories = ['oil', 'telecom', 'utilities', 'retail', 'health', 'real_estate', 'precious_metals', 'technology', 'finance', 'industrial', 'energy', 'materials']

def find_similar_words():
    broadened_category_lists = {}
    from nltk.corpus import wordnet as wn
    for predefined_category in predefined_categories:
        list = [predefined_category]
        for related_word_list in wn.synsets(predefined_category): # Each synset represents a diff concept.
            #list += related_word_list.lemma_names()
            for word in related_word_list.lemma_names():
                if word not in list:
                    list.append(word)
        
        broadened_category_lists[predefined_category] = list

    for category in broadened_category_lists:
        print(category)
        print(broadened_category_lists[category])  
    
    return broadened_category_lists

# broadened_category_lists = find_similar_words()

# manually edited down categories
broadened_category_lists = {
     "other": ['education', 'educational', 'crime'],
     "oil": ['oil', 'petroleum', 'crude_oil', 'crude', 'fossil_oil', 'fuel'],
     "telecom": ['telecom', 'telecommunication', '4g', '5g', 'phone', 'telephone'],
     "utilities": ['utilities', 'utility', 'energy', 'water'],
     "retail": ['retail', 'consumer'],
     "health": ['health', 'wellness', 'medicine','medical', 'drug', 'care', 'patient', 'cancer'],
     "real_estate": ['real_estate', 'real_property', 'realty', 'housing', 'houses', 'homes'],
     "precious_metals": ['precious_metal','gold', 'silver'],
     "technology": ['technology', 'engineering', 'computer', 'software', 'hardware'],
     "finance": ['finance', 'financial', 'invest', 'investment', 'bank'],
     "industrial": ['industrial', 'industry'],
     "energy": ['energy', 'coal', 'gas', 'solar', 'wind'],
     "materials": ['materials', 'material']
}

def tokenise(text):
    regex = re.compile('[^a-zA-Z]')
    tokens = []
    for sent in nltk.sent_tokenize(text):
        for word in nltk.word_tokenize(sent):
            clean_word = regex.sub('', word)
            if len(clean_word) > 1:
                tokens.append(clean_word.lower())
    return tokens

billTextList = get_all_bill_text()

def categorise_data(billTextList):
    tokenisedBillTextList = {}

    for billText in billTextList[0:2]:
        tokenisedBillTextList[billText.title] = tokenise(billText.desc)

    billTitleCategorisationMap = {}

    for billTitle in tokenisedBillTextList:
        print(billTitle)
        currentClassificationsCounts = {
        "other": 0, # put first in the case of a tie
        "oil": 0,
        "telecom": 0,
        "utilities": 0,
        "retail": 0,
        "health": 0,
        "real_estate": 0,
        "precious_metals": 0,
        "technology": 0,
        "finance": 0,
        "industrial": 0,
        "energy": 0,
        "materials": 0
    }
        tokens = tokenisedBillTextList[billTitle]
        #print(tokens)
        for token in tokens:
            #print(token)
            for key in currentClassificationsCounts:
                if token in broadened_category_lists[key]:
                    currentClassificationsCounts[key] = currentClassificationsCounts[key] + 1
        
        max_key = max(currentClassificationsCounts, key=currentClassificationsCounts.get)
        billTitleCategorisationMap[billTitle] = max_key

        return 

