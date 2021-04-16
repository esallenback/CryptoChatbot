import numpy as np
import tensorflow as tf
import keras
import model
import sys
import random

ERROR_THRESHOLD = 0.7

def main():
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
        x = model.bag_of_words(user_input)
        print(x)
        results = trained_model.predict([[x]])[0]
        print(results)

        results_index = np.argmax(results)
        
        if results[results_index] < ERROR_THRESHOLD:
            print("Sorry I didn't understand that, try again")
            continue

        tag = model.labels[results_index]

        for tg in model.json_data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']
                break
        print(random.choice(responses))

if __name__ == "__main__":
    main()