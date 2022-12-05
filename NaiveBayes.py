import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim.models import Word2Vec
import nltk.classify.util #calculates accuracy
from nltk.classify import NaiveBayesClassifier #imports the classifier Naive Bayes
from nltk.corpus import movie_reviews #imports movie reviews from nltk
from nltk.corpus import wordnet

file = open('trainData.txt', 'r', encoding="utf8")
alltext = file.read()
file.close()
alltext = alltext.replace("\n", " ")
sents = nltk.sent_tokenize(alltext)
words = word_tokenize(sents)
useful_words = [word for word in words if word not in stopwords.words('english')]

# This is how the Naive Bayes classifier expects the input
def create_word_features(words):
    useful_words = [word for word in words if word not in stopwords.words("english")]
    my_dict = dict([(word, True) for word in useful_words])
    return my_dict

neg_reviews = [] 

#loop over all the files in the neg folder and applies the create_word_features and same for negative reviews
for fileid in movie_reviews.fileids('neg'):
    words = movie_reviews.words(fileid)
    neg_reviews.append((create_word_features(words),"negative")) 

pos_reviews = []
for fileid in movie_reviews.fileids('pos'):
    
    words = movie_reviews.words(fileid)
    pos_reviews.append((create_word_features(words), "positive"))

trainrange = range(0,len(neg_reviews)*3/4)
testrange = range(len(neg_reviews)*3/4,0)
train_set = neg_reviews[trainrange] + pos_reviews[trainrange]
test_set =  neg_reviews[testrange] + pos_reviews[testrange]
    