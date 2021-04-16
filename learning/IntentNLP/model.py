import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.optimizers import SGD
import pandas as pd
import pickle
import random
import json 
import tensorflow as tf

stemmer = LancasterStemmer()

with open("intents.json") as json_file:
    json_data = json.load(json_file)

words = []
labels = []
docs_x = []
docs_y = []

# Tokenize inputs from the intents and organize them by tags

for intent in json_data["intents"]:
    for pattern in intent["patterns"]:
        pattern_words = nltk.word_tokenize(pattern)
        words.extend(pattern_words)
        docs_x.append(pattern_words)
        docs_y.append(intent["tag"])
    
    if intent["tag"] not in labels:
        labels.append(intent["tag"])

# Stem the tokenized input and remove duplicates

words = [stemmer.stem(w.lower()) for w in words if w != "?"]
words = sorted(list(set(words)))
labels = sorted(labels)

# Create a bag of words to vectorize words
if __name__ == "__main__":
    training = []
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []
        pattern_words = [stemmer.stem(w) for w in doc]

        for w in words:
            if w in pattern_words:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    # Convert primitive arrays into NP arrays

    # training = np.array(training)
    # output = np.array(output)

    model = Sequential()
    model.add(Dense(128, input_shape = (len(training[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(output[0]), activation='softmax'))

    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='binary_crossentropy', optimizer=sgd, metrics=['accuracy'])

    model.fit(np.array(training), np.array(output), epochs=200, batch_size=5, verbose=1)
    model.save("model.h5")

def bag_of_words(input):
    bag = [0 for _ in range(len(words))]
    input_words = nltk.word_tokenize(input)
    input_words = [stemmer.stem(word.lower()) for word in input_words]

    for i in input_words:
        for j, w in enumerate(words):
            if w == i:
                bag[j] = 1

    return np.array(bag)

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def chat():
    print("Start talking to the bot!")
    while True:
        user_input = input("You: ")
        if user_input == "exit":
            break
        # x = bag_of_words(user_input)
        x = bag_of_words(user_input)
        print(x.shape)
        results = model.predict([[x]])
        print(results)

# chat()