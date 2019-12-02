from numpy import array
from pickle import dump
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Embedding

from loader import Loader


class Trainer:
    @staticmethod
    def load_from_csv(name, delimiter, seq_size):
        doc = Loader.open_file(name, delimiter)
        tokens = Loader.clean_file(doc)
        lines = Loader.sequence_file(tokens, seq_size)
        return lines

    @staticmethod
    def load_file(filename):
        file = open(filename, 'r')
        text = file.read()
        file.close()
        return text

    @staticmethod
    def tokenize(lines):
        tokenizer = Tokenizer(filters='')
        tokenizer.fit_on_texts(lines)
        print(tokenizer.word_index)
        # Get vocabulary size
        vocab_size = len(tokenizer.word_index) + 1
        return tokenizer, vocab_size

    @staticmethod
    def sequence_data(tokenizer, lines, vocab_size):
        sequences = tokenizer.texts_to_sequences(lines)
        sequences = array(sequences)
        print(sequences.shape)
        x, y = sequences[:, :-1], sequences[:, -1]
        y = to_categorical(y, num_classes=vocab_size)
        seq_length = x.shape[1]
        return x, y, seq_length

    @staticmethod
    def build_model(vocab_size, seq_length):
        model = Sequential()
        model.add(Embedding(vocab_size, 50, input_length=seq_length))
        model.add(LSTM(100, return_sequences=True))
        model.add(LSTM(100))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(vocab_size, activation='softmax'))
        print(model.summary())
        return model

    @staticmethod
    def train_model(x, y, model, batch_size, epochs):
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        # fit model
        model.fit(x, y, batch_size=batch_size, epochs=epochs)
        return model

    @staticmethod
    def save_model(model, filename):
        model.save(filename)

    @staticmethod
    def save_tokenizer(tokenizer, filename):
        dump(tokenizer, open(filename, 'wb'))
