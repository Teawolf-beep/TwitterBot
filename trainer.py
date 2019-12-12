from numpy import array
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from pickle import dump
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Embedding, Dropout
from utils import mk_dir
from keras.callbacks import ModelCheckpoint
import os

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
        # Get vocabulary size
        vocab_size = len(tokenizer.word_index) + 1
        return tokenizer, vocab_size

    @staticmethod
    def sequence_data(tokenizer, lines, vocab_size):
        seq_length = 100
        sequences = tokenizer.texts_to_sequences(lines)
        sequences = array(sequences)
        print(sequences.shape)
        X, Y = sequences[:, :-1], sequences[:, -1]
        y = to_categorical(Y, num_classes=vocab_size)
        n_patterns = len(x)
        # reshape X to be [samples, time steps, features]
        x = np.reshape(X, (n_patterns, seq_length, 1))
        # normalize
        x = x / float(vocab_size)

        #seq_length = x.shape[1]
        return x, y, seq_length

    @staticmethod
    def build_model(x, y):
        print("building the model...")
        model = Sequential()
        model.add(LSTM(256, input_shape=(x.shape[1], x.shape[2]), return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(256))
        model.add(Dropout(0.2))
        model.add(Dense(y.shape[1], activation='softmax'))
        print(model.summary())
        return model
    
    '''@staticmethod
    def get_model(dropout=0.2):
    print('Build model...')
        model = Sequential()
        model.add(Embedding(input_dim=len(words), output_dim=1024))
        model.add(Bidirectional(LSTM(128)))
        if dropout > 0:
            model.add(Dropout(dropout))
        model.add(Dense(len(words)))
        model.add(Activation('softmax'))
        return model'''

    @staticmethod
    def train_model(x, y, model, batch_size, epochs):
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        
        # define the checkpoint
        mk_dir(checkpoints)
        filepath=os.path.join('checkpoints', 'weights-improvement-{epoch:02d}-{loss:.4f}.hdf5')
        checkpoint = ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min')
        callbacks_list = [checkpoint]
        
        # fit model
        model.fit_generator(x, y, batch_size=batch_size, epochs=epochs,
                            callbacks=callbacks_list)
                            validation_data=generator(sentences_test, labels_test, BATCH_SIZE),
                            validation_steps=int(len(sentences_test)/BATCH_SIZE) + 1))
        return model

    @staticmethod
    def save_model(model, filename):
        model.save(filename)

    @staticmethod
    def save_tokenizer(tokenizer, filename):
        dump(tokenizer, open(filename, 'wb'))
