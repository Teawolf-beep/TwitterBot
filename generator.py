import re
from pickle import load
import nltk.data
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences


class Generator:
    @staticmethod
    def generate_seq(model, tokenizer, seq_length, seed, min_word_count):
        result = list()
        in_text = seed
        count = 0
        while True:
            # Encode the text as integer
            encoded = tokenizer.texts_to_sequences([in_text])[0]
            # Truncate sequences to a fixed length
            encoded = pad_sequences([encoded], maxlen=seq_length)
            # Predict probabilities for each word
            yhat = model.predict_classes(encoded, verbose=0)
            out_word = ''
            for word, index in tokenizer.word_index.items():
                if index == yhat:
                    out_word = word
                    break

            in_text += ' ' + out_word
            if out_word == ';' and count >= min_word_count:
                break

            if out_word == '&amp':
                out_word = '&'

            if out_word != ';':
                result.append(out_word)

            count = count + 1

        return ' '.join(result)

    @staticmethod
    def postprocess(text):
        text = re.sub(r' i ', ' I ', text)
        text = re.sub(r'( \.)', '.', text)
        text = re.sub(r'( ,)', ',', text)
        text = re.sub(r'( !)', '!', text)
        text = re.sub(r'( \?)', r'\?', text)
        text = re.sub(r'( \()', r'\(', text)
        text = re.sub(r'( \))', r'\)', text)
        text = re.sub(r'( :)', ':', text)
        text = re.sub(r'(# )', '#', text)

        sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        text = sent_tokenizer.tokenize(text)
        text = [sent.capitalize() for sent in text]
        text = ' '.join(text)
        return text[:1].lower() + text[1:] + '!'

    @staticmethod
    def load_trained_model(filename):
        return load_model(filename)

    @staticmethod
    def load_tokenizer(filename):
        return load(open(filename, 'rb'))
