import numpy as np
from sklearn.model_selection import cross_validate
from nltk.corpus import movie_reviews
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import nltk.classify.util #calculates accuracy
from nltk.classify import NaiveBayesClassifier #imports the classifier Naive Bayes
from nltk.corpus import movie_reviews #imports movie reviews from nltk
from nltk.corpus import stopwords #imports stopwords from nltk
from nltk.corpus import wordnet
from nltk.corpus import movie_reviews
import nltk

all_words = movie_reviews.words()

sent = ""
#a token is a word or entity in a text
words = word_tokenize(sent)
useful_words = [word for word in words if word not in stopwords.words('english')]
print(useful_words)

def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words("english")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

neg_reviews = [] #We creates an empty list

#loop over all the files in the neg folder and applies the create_word_features
for fileid in movie_reviews.fileids('neg'):
    words = movie_reviews.words(fileid)
    neg_reviews.append((create_word_features(words),"negative")) 
    
print(len(neg_reviews))

pos_reviews = []
for fileid in movie_reviews.fileids('pos'):
    words = movie_reviews.words(fileid)
    pos_reviews.append((create_word_features(words), "positive"))
    
#print(pos_reviews[0])    
print(len(pos_reviews))