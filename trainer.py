from numpy import array
from pickle import dump
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Dropout


class Trainer:

    @staticmethod
    def load_file(filename):
        # Open a saved file with prepared text
        file = open(filename, 'r')
        text = file.read()
        file.close()
        return text

    @staticmethod
    def tokenize(lines):
        # One hot encode the passed text
        tokenizer = Tokenizer(filters='')
        tokenizer.fit_on_texts(lines)
        # Get vocabulary size
        vocab_size = len(tokenizer.word_index) + 1
        return tokenizer, vocab_size

    @staticmethod
    def sequence_data(tokenizer, lines, vocab_size):
        # Get sequences from tokenizer
        sequences = tokenizer.texts_to_sequences(lines)
        # Separate data into input and output
        sequences = array(sequences)
        x, y = sequences[:, :-1], sequences[:, -1]
        # One hot encode the output words for the input-output sequence pair
        y = to_categorical(y, num_classes=vocab_size)
        # Get length of input sequences
        seq_length = x.shape[1]
        return x, y, seq_length

    @staticmethod
    def build_model(vocab_size, seq_length):
        # Define the model
        model = Sequential()
        # Embedding layer
        model.add(Embedding(vocab_size, 50, input_length=seq_length))
        # Two LSTM hidden layer with 100 memory cells each
        model.add(LSTM(100, return_sequences=True))
        model.add(LSTM(100))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(vocab_size, activation='softmax'))
        # Print some information about the model
        print(model.summary())
        return model

    @staticmethod
    def train_model(x, y, model, batch_size, epochs):
        # Compile model
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        # Fit model
        model.fit(x, y, batch_size=batch_size, epochs=epochs)
        return model

    @staticmethod
    def save_model(model, filename):
        # Save the model
        model.save(filename)

    @staticmethod
    def save_tokenizer(tokenizer, filename):
        # Save the tokenizer
        dump(tokenizer, open(filename, 'wb'))
