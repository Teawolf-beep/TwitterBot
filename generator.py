import re
from pickle import load
import nltk.data
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


class Generator:
    @staticmethod
    def generate_seq(model, tokenizer, seq_length, seed, min_word_count, max_word_count):
        result = list()
        in_text = seed
        count = 0
        # Generate an output text in a loop
        while True:
            # Encode the text as integer numbers
            encoded = tokenizer.texts_to_sequences([in_text])[0]
            # Truncate sequences to a fixed length
            encoded = pad_sequences([encoded], maxlen=seq_length)
            # Predict probabilities for each word
            predicted = model.predict_classes(encoded, verbose=0)
            out_word = ''
            # Search for the predicted word in the tokenizer list
            for word, index in tokenizer.word_index.items():
                # True, if the word is found
                if index == predicted:
                    out_word = word
                    break

            # True, if the word equals the termination symbol and the count of generated words is big enough
            # or the generated sequence exceeds the maximum size
            if count >= max_word_count or (out_word == ';' and count >= min_word_count):
                # Abort generation
                break

            # Interchange the HTML ampersand for a regular ampersand
            if out_word == '&amp':
                out_word = '&'

            elif not out_word == ';':
                # Append the generated word to the final text and the input text
                result.append(out_word)
                in_text += ' ' + out_word
                # Increase the word count
                count = count + 1

        return ' '.join(result)

    @staticmethod
    def postprocess(text):
        # Make every single 'i' uppercase
        text = re.sub(r' i ', ' I ', text)
        # Remove space characters before certain symbols
        text = re.sub(r'( \.)', '.', text)
        text = re.sub(r'( ,)', ',', text)
        text = re.sub(r'( !)', '!', text)
        text = re.sub(r'( \?)', r'\?', text)
        text = re.sub(r'( \()', r'\(', text)
        text = re.sub(r'( \))', r'\)', text)
        text = re.sub(r'( :)', ':', text)
        text = re.sub(r'(# )', '#', text)

        # Use nltk (natural language toolkit) to write the beginnings of sentences uppercase
        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        text = sent_tokenizer.tokenize(text)
        text = [sent.capitalize() for sent in text]
        text = ' '.join(text)
        # Make the first word lowercase again, append an exclamation mark!
        return text[:1].lower() + text[1:]

    @staticmethod
    def load_trained_model(filename):
        # Load a trained model
        return load_model(filename)

    @staticmethod
    def load_tokenizer(filename):
        # Load a tokenizer
        return load(open(filename, 'rb'))
