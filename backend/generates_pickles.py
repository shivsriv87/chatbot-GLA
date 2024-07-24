import json
import pickle
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

words = []
classes = []
documents = []
ignore_words = ['?', '!', '.', ',']

# Loop through each sentence in our intents patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word in the sentence
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Add documents in the corpus
        documents.append((w, intent['tag']))
        # Add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize, lower each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# Sort classes
classes = sorted(list(set(classes)))

# Save the words and classes to a pickle file
pickle.dump(words, open('backend/back/words.pkl', 'wb'))
pickle.dump(classes, open('backend/back/classes.pkl', 'wb'))

print(f"Number of words: {len(words)}")
print(f"Number of classes: {len(classes)}")
