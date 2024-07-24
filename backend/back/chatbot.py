import random
import json
import pickle
import numpy as np
import tensorflow as tf
import nltk
from nltk.stem import WordNetLemmatizer
import os

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Initialize the lemmatizer and load the necessary files
lemmatizer = WordNetLemmatizer()
with open('back/intents.json', encoding='utf8') as f:
    intents = json.load(f)

words = pickle.load(open('back/words.pkl', 'rb'))
classes = pickle.load(open('back/classes.pkl', 'rb'))

# Ensure the length of words matches the model's expected input size
print(f"Number of words in words.pkl: {len(words)}")
expected_input_size = len(words)  # Dynamically get the size from words.pkl

# Construct an absolute path to the model file correctly
current_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(current_dir, 'chatbot_model.h5')

try:
    model = tf.keras.models.load_model(model_path)
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None  # Define model as None to handle the error gracefully

def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * expected_input_size  # Adjust the size to match the model's expected input shape
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    if model is None:
        return "Model is not loaded."

    bow = bag_of_words(sentence)
    print("Bag of Words:", bow)  # Debug statement to print bag of words

    bow = np.array([bow], dtype=np.float32)  # Ensure the input is of shape (1, len(words)) with the correct dtype
    print("Input to model:", bow)

    res = model.predict(bow)
    print("Model predictions:", res)  # Debug statement to print model predictions

    res = res[0]  # Ensure it's the correct shape
    error_threshold = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > error_threshold]

    print("Results after thresholding:", results)  # Debug statement to print results after thresholding

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        if r[0] < len(classes):
            return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})

    print("Return list:", return_list)  # Debug statement to print return list

    if return_list:
        tag = return_list[0]['intent']
        print("Predicted intent:", tag)
        list_of_intents = intents['intents']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                print("Response:", result)
                return result
    print("Default response")
    return "Sorry, I don't understand your query."
