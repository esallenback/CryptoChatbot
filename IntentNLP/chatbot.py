import numpy as np
import tensorflow as tf
import keras
import model
import sys

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
        results = trained_model.predict([[x]])
        print(results)

if __name__ == "__main__":
    main()