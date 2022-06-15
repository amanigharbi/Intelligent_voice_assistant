import tflearn
import tensorflow as tf
import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.embedding_ops import embedding
from tflearn.layers.recurrent import bidirectional_rnn, BasicLSTMCell
from tflearn.layers.estimator import regression

stemmer = LancasterStemmer() #stemmer to get stem of a word. ex. 'say' would be stem word of 'saying'.
#  LSTM RNN
def recurrent_neural_network(X, y):
    tf.compat.v1.reset_default_graph() #Clears the default graph stack and resets the global default graph
# neural network's layers
    network = tflearn.input_data(shape= [None, len(X[0])]) #input layer
    network = tflearn.embedding(network, 8,len(y[0])) #1st hidden layer
    network = tflearn.lstm(network, len(y[0]), dropout=0.8)
    network = tflearn.fully_connected(network, 8,activation='softmax') #2nd hidden layer
#     network = tflearn.fully_connected(network, len(y[0]), activation= 'softmax') #output layer
    network = tflearn.regression(network, optimizer='adam', learning_rate=0.001, loss='categorical_crossentropy')
    model = tflearn.DNN(network, tensorboard_dir='tflearn_logs') #tensorboard_dir is path to store logs
    return model
# LSTM
def define_network(X, y):
    tf.compat.v1.reset_default_graph() #Clears the default graph stack and resets the global default graph
# neural network's layers
    network = tflearn.input_data(shape= [None, len(X[0])]) #input layer
    network = tflearn.fully_connected(network, 8) #1st hidden layer
    network = tflearn.fully_connected(network, 8) #2nd hidden layer
    network = tflearn.fully_connected(network, len(y[0]), activation= 'softmax') #output layer
    network = tflearn.regression(network)
    model = tflearn.DNN(network, tensorboard_dir='tflearn_logs') #tensorboard_dir is path to store logs
    return model
# convolutional network
def convolutional_network(X, y):
    tf.compat.v1.reset_default_graph() #Clears the default graph stack and resets the global default graph
# neural network's layers
    network = tflearn.input_data(shape=[None, len(X[0])], name='input')
    network = tflearn.embedding(network, input_dim=len(X[0]), output_dim=len(y[0]))
    branch1 = tflearn.conv_1d(network, len(y[0]), 3, padding='valid', activation='relu', regularizer="L2")
    branch2 = tflearn.conv_1d(network, len(y[0]), 4, padding='valid', activation='relu', regularizer="L2")
    branch3 = tflearn.conv_1d(network, len(y[0]), 5, padding='valid', activation='relu', regularizer="L2")
    network = tflearn.merge([branch1, branch2, branch3], mode='concat', axis=1)
#     network = tf.expand_dims(network, 2)
    network = tf.global_max_pool(network)
    network = tflearn.dropout(network, 0.5)
    network = tflearn.fully_connected(network, len(y[0]), activation= 'softmax') #output layer
    network = tflearn.regression(network, optimizer='adam', learning_rate=0.001,
                     loss='categorical_crossentropy', name='target')
# Training
    model = tflearn.DNN(network, tensorboard_verbose=0)
    return model
# bidirectional_rnn
def bidirectional_rnn(X, y):
    tf.compat.v1.reset_default_graph() #Clears the default graph stack and resets the global default graph
# neural network's layers
    network = input_data(shape= [None, len(X[0])]) #input layer
    network = embedding(network, input_dim=len(X[0]), output_dim=len(y[0])) #1st hidden layer
    network = bidirectional_rnn(network, BasicLSTMCell(len(y[0])))
    network = dropout(net, 0.5)
    network = fully_connected(network, len(y[0]), activation= 'softmax') #output layer
    network = regression(network,optimizer='adam', loss='categorical_crossentropy')
    model = tflearn.DNN(network, tensorboard_dir='tflearn_logs') #tensorboard_dir is path to store logs
    return model
# gives stemmed, tokenized words list from sentence pattern without words in ignore_words list
def clean_pattern(pattern, ignore_words):
    stemmed_pattern = []
    wrds = nltk.word_tokenize(pattern)
    for w in wrds:
        if w not in ignore_words:
            stemmed_pattern.append(stemmer.stem(w.lower()))
    return stemmed_pattern

# generates a numpy array of 0 & 1 from string sentence of user to fed to model
def bag_of_words(sentence, stemmed_words, ignore_words):
    bag = []
    stemmed_pattern = clean_pattern(sentence, ignore_words)
    for w in stemmed_words:
        if w in stemmed_pattern:
            bag.append(1)
        else:
            bag.append(0)
    return np.array(bag)