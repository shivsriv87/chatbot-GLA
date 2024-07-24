import json
import random
import numpy as np
import pickle
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD
import nltk
from nltk.stem import WordNetLemmatizer

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')

# Initialize the lemmatizer
lemmatizer = WordNetLemmatizer()

# Load the intents file
with open('backend/back/intents.json', encoding='utf8') as f:
    intents = json.load(f)

# Initialize data lists
words = []
classes = []
documents = []
ignore_words = ['?', '!', '.', ',']

# Process each sentence in the intents file
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word in the sentence
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        # Add to documents
        documents.append((word_list, intent['tag']))
        # Add to classes if it's not already there
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize, lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# Sort classes
classes = sorted(list(set(classes)))

# Create pickle files
pickle.dump(words, open('backend/back/words.pkl', 'wb'))
pickle.dump(classes, open('backend/back/classes.pkl', 'wb'))

# Initialize training data
training = []
output_empty = [0] * len(classes)

# Create training set
for doc in documents:
    # Initialize the bag of words
    bag = []
    # List of tokenized words for the pattern
    pattern_words = doc[0]
    # Lemmatize each word
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]
    # Create our bag of words array with 1, if word match found in current pattern
    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    # Output is a '0' for each tag and '1' for current tag
    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

# Shuffle the features and convert into np.array
random.shuffle(training)
training = np.array(training, dtype=object)  # Ensure that dtype is object to avoid issues with varying lengths

# Create train and test lists
train_x = np.array([np.array(i) for i in list(training[:, 0])])
train_y = np.array([np.array(i) for i in list(training[:, 1])])

# Create model - 3 layers. First layer 128 neurons, second layer 64 neurons and 3rd output layer with number of neurons
# equal to number of intents to predict output intent with softmax
model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

# Compile model. Stochastic gradient descent with Nesterov accelerated gradient gives good results for this model
sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

# Fit the model
hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('backend/back/chatbot_model.h5', hist)

print("Model created and saved successfully")
