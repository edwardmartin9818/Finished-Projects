import numpy as np
import nltk
import random
import operator
import sklearn
import string
import os
import sys
from random import randrange
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.metrics import precision_score,recall_score,f1_score,accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MaxAbsScaler

if len(sys.argv) < 2:
    rand = randrange(50)
else:
    rand = sys.argv[1]


nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

def test_model(model, testdata):
    print("Beginning testing...")
    X_test = testdata[0]
    Y_test = testdata[1]

    predictions = model.predict(X_test)

    print(classification_report(Y_test, predictions))
    precision=precision_score(Y_test, predictions, average='macro')
    recall=recall_score(Y_test, predictions, average='macro')
    f1=f1_score(Y_test, predictions, average='macro')
    accuracy=accuracy_score(Y_test, predictions)

    print ("Precision: "+str(round(precision,5)))
    print ("Recall: "+str(round(recall,5)))
    print ("F1-Score: "+str(round(f1,5)))
    print ("Accuracy: "+str(round(accuracy,5)))

    return precision, recall, f1, accuracy


#RETRIEVING DATA---------------------------------------------------
datafile_dict = {}
datafile_dict["business"] = 510
datafile_dict["entertainment"] = 386
datafile_dict["politics"] = 417
datafile_dict["sport"] = 511
datafile_dict["tech"] = 401

keys = ["business", "entertainment","politics", "sport", "tech"]

data_business_raw = []
data_entertainment_raw = []
data_politics_raw = []
data_sport_raw = []
data_tech_raw = []

cwd = str(os.getcwd())

for key in datafile_dict:
    paths = []
    num_data = datafile_dict[key]
    count = 1
    for i in range(num_data):
        if count < 10:
            path = cwd + "\\data\\bbc\\" + key +"\\00" + str(count) + ".txt"
        elif count < 100:
            path = cwd + "\\data\\bbc\\" + key +"\\0" + str(count) + ".txt"
        else:
            path = cwd + "\\data\\bbc\\" + key +"\\" + str(count) + ".txt"
        count += 1
        paths.append(path)  
    print("Grabbing " + key +" data...")
    data_list_raw = []
    for path in paths:
        with open(path, encoding="utf8", errors='ignore') as f:
            data_list_raw.append(f.readlines())

    if key == "business": data_business_raw = data_list_raw
    elif key == "entertainment": data_entertainment_raw = data_list_raw
    elif key == "politics": data_politics_raw = data_list_raw
    elif key == "sport": data_sport_raw = data_list_raw
    elif key == "tech": data_tech_raw = data_list_raw
  
print("Number of business articles: ", len(data_business_raw))
print("Number of entertainment articles: ", len(data_entertainment_raw))
print("Number of politics articles: ", len(data_politics_raw))
print("Number of sport articles: ", len(data_sport_raw))
print("Number of tech articles: ", len(data_tech_raw))
print("Deleting duplicated data...")
data_business = []
data_entertainment = []
data_politics = []
data_sport = []
data_tech = []

#REMOVE REPLICATED DATA

for i, article1 in enumerate(data_business_raw):
  for j, article2 in enumerate(data_business_raw):
    if i == j: continue
    elif article1 == article2:
      count += 1
      del data_business_raw[j]
  

for i, article1 in enumerate(data_entertainment_raw):
  for j, article2 in enumerate(data_entertainment_raw):
    if i == j: continue
    elif article1 == article2:
      count += 1
      del data_entertainment_raw[j]

for i, article1 in enumerate(data_politics_raw):
  for j, article2 in enumerate(data_politics_raw):
    if i == j: continue
    elif article1 == article2:
      count += 1
      del data_politics_raw[j]

for i, article1 in enumerate(data_sport_raw):
  for j, article2 in enumerate(data_sport_raw):
    if i == j: continue
    elif article1 == article2:
      count += 1
      del data_sport_raw[j]

for i, article1 in enumerate(data_tech_raw):
  for j, article2 in enumerate(data_tech_raw):
    if i == j: continue
    elif article1 == article2:
      count += 1
      del data_tech_raw[j]


print("Data grabbed.\n")
print("Number of business articles: ", len(data_business_raw))
print("Number of entertainment articles: ", len(data_entertainment_raw))
print("Number of politics articles: ", len(data_politics_raw))
print("Number of sport articles: ", len(data_sport_raw))
print("Number of tech articles: ", len(data_tech_raw))
print("Number of deleted duplicate articles: ", count,"\n")

labels = []

for i in range(len(data_business_raw)):
  labels.append(0)

for i in range(len(data_entertainment_raw)):
  labels.append(1)

for i in range(len(data_politics_raw)):
  labels.append(2)

for i in range(len(data_sport_raw)):
  labels.append(3)

for i in range(len(data_tech_raw)):
  labels.append(4)

labels = np.asarray(labels)

all_data_raw = []
all_data_raw = (data_business_raw + data_entertainment_raw + data_politics_raw + data_sport_raw + data_tech_raw)

stopwords=set(nltk.corpus.stopwords.words('english'))
stopwords.add(".")
stopwords.add(",")
stopwords.add("``")
stopwords.add("''")
stopwords.add("'s")
stopwords.add("-")
stopwords.add("(")
stopwords.add(")")
stopwords.add(":")
stopwords.add("'")
stopwords.add("''")
stopwords.add("!")

print("Beginning feature creation...")

#FAILED FEATURES-----------------------------------------------

#POS Tagging---------------------------------------------------
#all_tokens = []
#lemmatizer = nltk.stem.WordNetLemmatizer()
#nltk.download('averaged_perceptron_tagger')

#for article in all_data_raw:
#  list_tokens = []
#  for line in article[1:]:
#    sentence_split = nltk.tokenize.sent_tokenize(str(line))
#    for sentence in sentence_split:
#      list_tokens_sentence = nltk.tokenize.word_tokenize(sentence)
#      for token in list_tokens_sentence:
#        list_tokens.append(token.lower())
#  all_tokens.append(list_tokens)

#all_tagged_tokens = []
#for article in all_tokens:
#  all_tagged_tokens.append(nltk.pos_tag(article))

#tags = ["IN","JJ","JJR","JJS","MD","NN","NNP","NNS","PRP","RB","RBR","RBS","UH","VB","VBD","VBN","VBP","VBZ","$","£"]
#feature_8 = []
#for article in all_tagged_tokens:
#  article_count = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#  for j, tag in enumerate(tags):
#    for i, pair in enumerate(article):
#      if pair[1] == tag: article_count[j] += 1

#  feature_8.append(article_count)

#print(feature_8[0])
#tfidf_transformer = TfidfTransformer().fit(feature_8) #By default this is using the 'l2' norm
#feature_8_tf = tfidf_transformer.transform(feature_8).toarray()
#scaler = MaxAbsScaler()
#feature_8 = scaler.fit_transform(feature_8_tf)
#print(feature_8[0])
#--------------------------------------------------------
#ZONED word-frequency vectors----------------------------

#all_tokens_title = []
#all_tokens_body = []
#lemmatizer = nltk.stem.WordNetLemmatizer()

#for article in all_data_raw:
#  list_tokens = []
#  # print("Art: ", article)
#  sentence_split = nltk.tokenize.sent_tokenize(str(article[0]))
#  # print("List of sent: ", sentence_split)
#  for sentence in sentence_split:
#    # print("Sentence: ", sentence)
#    list_tokens_sentence = nltk.tokenize.word_tokenize(sentence.translate(str.maketrans('', '', string.punctuation))) #Strips away punctation
#    for token in list_tokens_sentence:
#      # print("tokens: ",token)
#      list_tokens.append(lemmatizer.lemmatize(token.lower()))

#  all_tokens_title.append(list_tokens)

#  list_tokens = []
#  for line in article[1:]:
#    # print("Line: ", line)
#    sentence_split = nltk.tokenize.sent_tokenize(str(line))
#    # print("List of sent: ", sentence_split)
#    for sentence in sentence_split:
#      # print("Sentence: ", sentence)
#      list_tokens_sentence = nltk.tokenize.word_tokenize(sentence.translate(str.maketrans('', '', string.punctuation))) #Strips away punctation
#      for token in list_tokens_sentence:
#        # print("tokens: ",token)
#        list_tokens.append(lemmatizer.lemmatize(token.lower()))

#  all_tokens_body.append(list_tokens)

#FOR TITLE
#mf_title = None
#kbest_title = 2000
#count_vector_title = CountVectorizer(input='content',decode_error='ignore',
#                               stop_words=stopwords, 
#                               max_features=mf_title,
#                               analyzer=lambda x: x)

#feature_title = count_vector_title.fit_transform(all_tokens_title)
#feature_title_kb = SelectKBest(chi2, k=kbest_title).fit_transform(feature_title, labels)
#tfidf_transformer = TfidfTransformer().fit(feature_title_kb) #By default this is using the 'l2' norm
#feature_title_tf = tfidf_transformer.transform(feature_title_kb).toarray()

#FOR BODY
#mf_body = None
#kbest_body = 2000
#count_vector_body = CountVectorizer(input='content',decode_error='ignore',
#                               stop_words=stopwords, 
#                               max_features=mf_body,
#                               analyzer=lambda x: x)
#
#feature_body = count_vector_body.fit_transform(all_tokens_body)
#feature_body_kb = SelectKBest(chi2, k=kbest_body).fit_transform(feature_body, labels)
#tfidf_transformer = TfidfTransformer().fit(feature_body_kb) #By default this is using the 'l2' norm
#feature_body_tf = tfidf_transformer.transform(feature_body_kb).toarray()
#--------------------------------------------------------------------------------
#AVERAGE WORD LENGTH
#feature_length = []

#for article in all_data_raw:
#  count = 0
#  list_tokens = []
#  for line in article:
#    # print("Line: ", line)
#    sentence_split = nltk.tokenize.sent_tokenize(str(line))
#    # print("List of sent: ", sentence_split)
#    for sentence in sentence_split:
#      # print("Sentence: ", sentence)
#      list_tokens_sentence = nltk.tokenize.word_tokenize(sentence.translate(str.maketrans('', '', string.punctuation))) #Strips away punctation
#      for token in list_tokens_sentence:
#        # print("tokens: ",token)
#        count += len(token)
#        list_tokens.append(token.lower())
#  feature_length.append(count/len(list_tokens))

#feature_length = np.asarray(feature_length)
#print(feature_length.shape)
#print(feature_length[0])
#scaler = StandardScaler().fit(feature_length.reshape(-1,1))
#feature_length_scaled = scaler.transform(feature_length.reshape(-1,1))
#print(feature_length_scaled.shape)
#print(feature_length_scaled[500])
#------------------------------------------------


#SUCCESSFUL FEATURES -------------------------------------------------------------
#CREATE PAIRS FEATURE
all_pairs_tokens = []
lemmatizer = nltk.stem.WordNetLemmatizer()

for article in all_data_raw:
  list_tokens = []
  for line in article:
    sentence_split = nltk.tokenize.sent_tokenize(str(line))
    for sentence in sentence_split:
      list_tokens_sentence = nltk.tokenize.word_tokenize(sentence.translate(str.maketrans('', '', string.punctuation))) #Strips away punctation
      for i, token in enumerate(list_tokens_sentence):
        if i >= 1:
          pair = list_tokens_sentence[i-1] + " " + list_tokens_sentence[i] 
          list_tokens.append(lemmatizer.lemmatize(pair.lower()))
  all_pairs_tokens.append(list_tokens)

mf_all_pairs = None
kbest_all_pairs = 1000
count_vector_all_pairs = CountVectorizer(input='content',decode_error='ignore',
                               stop_words=stopwords, 
                               max_features=mf_all_pairs,
                               analyzer=lambda x: x)
feature_all_pairs = count_vector_all_pairs.fit_transform(all_pairs_tokens)
tfidf_transformer = TfidfTransformer().fit(feature_all_pairs) #By default this is using the 'l2' norm
features_all_pairs_final = tfidf_transformer.transform(feature_all_pairs).toarray()
features_all_pairs_final_kb = SelectKBest(chi2, k=200).fit_transform(features_all_pairs_final, labels)
#--------------------------------------------------------------------

#CREATE LENGTH FEATURE--------------------------------------------
feature_length = []

for article in all_data_raw:
  list_tokens = []
  for line in article:
    sentence_split = nltk.tokenize.sent_tokenize(str(line))
    for sentence in sentence_split:
      list_tokens_sentence = nltk.tokenize.word_tokenize(sentence.translate(str.maketrans('', '', string.punctuation))) #Strips away punctation
      for token in list_tokens_sentence:
        list_tokens.append(token.lower())
  feature_length.append(len(list_tokens))

feature_length = np.asarray(feature_length)
scaler = MaxAbsScaler().fit(feature_length.reshape(-1,1))
feature_length_final = scaler.transform(feature_length.reshape(-1,1))
#--------------------------------------------------------------



#CREATE SINGLES FEATURE----------------------------------------
all_tokens = []
lemmatizer = nltk.stem.WordNetLemmatizer()

for article in all_data_raw:
  list_tokens = []
  for line in article:
    sentence_split = nltk.tokenize.sent_tokenize(str(line))
    for sentence in sentence_split:
      list_tokens_sentence = nltk.tokenize.word_tokenize(sentence.translate(str.maketrans('', '', string.punctuation))) #Strips away punctation
      for token in list_tokens_sentence:
        list_tokens.append(lemmatizer.lemmatize(token.lower()))
  all_tokens.append(list_tokens)

count_vector = CountVectorizer(input='content',decode_error='ignore',
                               stop_words=stopwords, 
                               max_features=None,
                               analyzer=lambda x: x)
feature = count_vector.fit_transform(all_tokens)
tfidf_transformer = TfidfTransformer().fit(feature) #By default this is using the 'l2' norm
feature_final = tfidf_transformer.transform(feature).toarray()
feature_final_kb = SelectKBest(chi2, k=1200).fit_transform(feature_final, labels)
#------------------------------------------------------------------

print("Features created.\n")


#MODEL CREATION---------------------------------------------------
if sys.argv != None:
    rand = randrange(50)
else:
    rand = sys.argv
#Note, random state '26' was used to produce the results in the report
feature_second = np.append(feature_final_kb, features_all_pairs_final_kb, axis=1)
feature_second = np.append(feature_second, feature_length_final, axis=1)

X_train, X_test, Y_train, Y_test = train_test_split(feature_second, labels, test_size=0.3, random_state=rand)
X_test, X_dev, Y_test, Y_dev = train_test_split(X_test, Y_test, test_size=0.5, random_state=rand)
print("Beginning model training...")
model = sklearn.svm.SVC(kernel='rbf', gamma='scale')
model.fit(X_train, Y_train)
print("Model trained.\n")
print("Below is the test results using the development set:")
p, r, f, a = test_model(model, [X_dev, Y_dev])
print("Below is the test results using the unseen test set:")
p, r, f, a = test_model(model, [X_test, Y_test])
#-----------------------------------------------------------------





