from __future__ import print_function
from numpy import array
import numpy as np
from keras import Input
from tensorflow import keras
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.text import Tokenizer
from pickle import dump
from keras.callbacks import LearningRateScheduler, ModelCheckpoint, TensorBoard, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU, Activation
from tensorflow.keras.layers import LSTM, Bidirectional
from tensorflow.keras.layers import Embedding, Dropout
from utils import mk_dir
from keras.callbacks import ModelCheckpoint
import os
from keras.optimizers import Adam


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
        x, Y = sequences[:, :-1], sequences[:, -1]
        y = to_categorical(Y, num_classes=vocab_size)
        n_patterns = len(x)
        # reshape X to be [samples, time steps, features]
        #x = np.reshape(X, (n_patterns, seq_length, 1))
        # normalize
        #x = X / float(vocab_size)

        #seq_length = x.shape[1]
        return x, y, seq_length

    @staticmethod
    def bidirectional_lstm_model(seq_length, vocab_size):
        print('Build LSTM model.')
        model = Sequential()
        model.add(Embedding(vocab_size, 128, input_length=seq_length))
        model.add(Bidirectional(LSTM(128)))
        #model.add(Dropout(0.6))
        model.add(Dense(vocab_size, activation='softmax'))
        return model
    
    
    '''def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                    batch_input_shape=[batch_size, None]),
            tf.keras.layers.GRU(rnn_units,
                                return_sequences=True,
                                stateful=True,
                                recurrent_initializer='glorot_uniform'),
            tf.keras.layers.Dense(vocab_size)
        ])
        return model
            
    def build_model(x, y):
        print("building the model...")
        model = Sequential()
        model.add(Embedding(vocab_size, 50, input_length=seq_length))
        model.add(LSTM(100, return_sequences=True))
        model.add(LSTM(100))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(vocab_size, activation='softmax'))
        print(model.summary())
        return model
    
    @staticmethod
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
    def train_model(x, y, model, batch_size, epochs, patience=10):
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['categorical_accuracy'])
        
        # define the checkpoint
        mk_dir("checkpoints")
        early_stop = EarlyStopping('val_loss', patience=patience)
        reduce_lr = ReduceLROnPlateau(verbose=1, epsilon=0.001,
                                    patience=int(patience/2))
        filepath=os.path.join('checkpoints', 'weights-improvement-{epoch:02d}-{loss:.4f}.hdf5')
        callbacks = [ModelCheckpoint(filepath, monitor='val_loss', verbose=1, save_best_only=True, mode='min'),
                    reduce_lr, early_stop]
                
        # fit model
        history = model.fit(x, y, batch_size=batch_size, epochs=epochs,
                            callbacks=(callbacks),
                            shuffle=True,
                            validation_split=0.01)
        return model, history


    @staticmethod
    def plot(history, plot=True):
        if plot:
            hist_path='plot-results/history.h5'
            input_dir = os.path.dirname(hist_path)
            plt.figure(figsize=(8,8))
            plt.plot(history.history['loss'], label='train')
            plt.plot(history.history['val_loss'], label='validation')
            plt.xlabel("number of epochs")
            plt.ylabel("loss")
            plt.legend()
            plt.title('loss_function')
            plt.savefig(os.path.join(input_dir, "loss.png"))
            plt.show()
            
            plt.figure(figsize=(8,8))
            plt.plot(history.history['accuracy'], label = 'train')
            plt.plot(history.history['val_accuracy'], label = 'valid')
            plt.legend()
            plt.xlabel("number of epochs")
            plt.ylabel("accuracy")
            plt.title('Accuracy')
            plt.savefig(os.path.join(input_dir, "accuracy.png"))
            plt.show()

    @staticmethod
    def save_model(model, filename):
        model.save(filename)

    @staticmethod
    def save_tokenizer(tokenizer, filename):
        dump(tokenizer, open(filename, 'wb'))
