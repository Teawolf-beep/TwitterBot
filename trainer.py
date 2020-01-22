from numpy import array
from pickle import dump
from matplotlib import pyplot
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint

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
        file = open(filename, 'r', encoding="utf8")
        text = file.read()
        file.close()
        return text

    @staticmethod
    def tokenize(lines):
        tokenizer = Tokenizer(filters='')
        tokenizer.fit_on_texts(lines)
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
        model.add(Dropout(0.2))
        model.add(Bidirectional(LSTM(100, return_sequences=True)))
        model.add(Dropout(0.2))
        model.add(Bidirectional(LSTM(100)))
        model.add(Dropout(0.2))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(vocab_size, activation='softmax'))
        print(model.summary())
        return model

    @staticmethod
    def train_model(x, y, model, batch_size, epochs):
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        
        early_stop = EarlyStopping('val_loss', patience=5)

        # fit model
        history = model.fit(x, y, batch_size=batch_size, callbacks=[early_stop], epochs=epochs, validation_split=0.1)
        pyplot.plot(history.history['loss'])
        pyplot.plot(history.history['val_loss'])
        pyplot.title('model train vs validation loss')
        pyplot.ylabel('loss')
        pyplot.xlabel('epoch')
        pyplot.legend(['train', 'validation'], loc='upper right')
        pyplot.show()
        return model

    @staticmethod
    def save_model(model, filename):
        model.save(filename)

    @staticmethod
    def save_tokenizer(tokenizer, filename):
        dump(tokenizer, open(filename, 'wb'))
