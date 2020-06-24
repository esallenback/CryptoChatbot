import numpy as np
import tensorflow as tf
import keras
import model
import sys
import random
import os

ERROR_THRESHOLD = 0.92

def main(modelName = "model.h5"):
    print("Loading crypto names...")
    currency_file = open("currencyList.txt", "r")
    currency_list = currency_file.read().splitlines()
    currency_file.close()
    print("Crypto names loaded!")
    for currency in currency_list:
        print(currency)
    print("Loading model...")
    try:
        trained_model = keras.models.load_model("model.h5")
    except:
        print("Model not found!")
        print("Compile the model by running model.py")
        sys.exit(1)
    print("Model loaded!")
    print(trained_model.summary())
    print("Start talking to the bot!")
    while True:
        user_input = input("You: ")
        if user_input == "exit":
            break
        # x = bag_of_words(user_input)
        print("")
        x = model.bag_of_words(user_input)
        print(x)
        results = trained_model.predict([[x]])[0]
        # print(results)

        results_index = np.argmax(results)
        
        if results[results_index] < ERROR_THRESHOLD:
            print("Sorry I didn't understand that, try again")
            continue

        for i in range(len(results)):
            print(str(results[i]) + " -> " + str(model.labels[i]))

        tag = model.labels[results_index]

        for tg in model.json_data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                break
        # Now we have the action intent of the query
        found = False
        for currency in currency_list:
            if (currency in user_input.split()):
                print("Query currency = " + currency)
                found = True
                break
        if found == False:
            print("Error: Could not find currency type in query!")
        print("")
        print("Chatbot: " + str(random.choice(responses)))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        main()
    else:
        main(sys.argv[1])