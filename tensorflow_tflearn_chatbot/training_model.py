import numpy as np
import tflearn
import tensorflow as tf
import random
import json
import pickle
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from utils import clean_pattern, define_network, recurrent_neural_network , convolutional_network , bidirectional_rnn
data_file = open('intents.json', encoding='utf-8').read()
data = json.loads(data_file)
# Some cleaning of data in intents.json
stemmed_words = []
tags = []
ignore_words = ['!', '?', '.']
corpus = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        stemmed_pattern = clean_pattern(pattern, ignore_words)
        stemmed_words.extend(stemmed_pattern)
        corpus.append((stemmed_pattern, intent['tag']))
    if intent['tag'] not in tags:
        tags.append(intent['tag'])

# remove duplicates and sort
stemmed_words = sorted(list(set(stemmed_words)))
tags = sorted(list(set(tags)))
print(len(stemmed_words))
print(len(tags))
print(len(corpus))
print(stemmed_words)
print(tags)
print(corpus)
# Creating numeric features and labels out of cleaned data
X = []
y = []
for item in corpus:
    bag = [] #array of 1 and 0. 1 if stemmed word is present in stemmed pattern
    stemmed_pattern = item[0]
    for w in stemmed_words:
        if w in stemmed_pattern:
            bag.append(1)
        else:
            bag.append(0)

    tags_row = [] #array of 1 and 0. 1 for current tag and for everything else 0.
    current_tag = item[1]
    for tag in tags:
        if tag == current_tag:
            tags_row.append(1)
        else:
            tags_row.append(0)

    #for each item in corpus, X will be array indicating stemmed words and y array indicating tags
    X.append(bag)
    y.append(tags_row)

X = np.array(X)
y = np.array(y)
print(X)
print(y)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)

# saving variables in pickle to be used by main.py
with open('saved_variables.pickle', 'wb') as file:
    pickle.dump((stemmed_words, tags, ignore_words, X, y), file)
    # model = recurrent_neural_network(X, y)
model = define_network(X_train, y_train)
# model = convolutional_network(X, y)
# model = bidirectional_rnn(X, y)
#print("train")
hist=model.fit(X_train, y_train, n_epoch=200, batch_size=8, show_metric=True)
#print("test")
hist1=model.fit(X_test, y_test, n_epoch=200, batch_size=8, show_metric=True)
plt.plot(hist.history['acc'])
plt.plot(hist1.history['acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(hist.history['loss'])
plt.plot(hist1.history['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
model.save("chatbot_model.tflearn")