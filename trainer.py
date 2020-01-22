from numpy import array
from matplotlib import pyplot
from tensorflow import keras
from pickle import dump
from keras.callbacks import LearningRateScheduler, ModelCheckpoint, TensorBoard, EarlyStopping, ReduceLROnPlateau, LambdaCallback
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Embedding
from keras.layers import Bidirectional
from keras.layers import Dropout
from keras.optimizers import Adam

from utils import mk_dir
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
        model.add(Bidirectional(LSTM(64, return_sequences=True)))
        model.add(LSTM(128, return_sequences=True))
        #model.add(Dropout(0.5))
        model.add(LSTM(128))
        #model.add(Dropout(0.5))
        model.add(Dense(100, activation='relu'))
        model.add(Dense(vocab_size, activation='softmax'))
        print(model.summary())
        return model

    @staticmethod
    def train_model(x, y, model, batch_size, epochs, patience=10):
        # learning rate in adam ändern und vllt mal sgd ausprobieren
        opt = Adam(lr=0.001)
        model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

        early_stop = EarlyStopping('val_loss', patience=patience)
        reduce_lr = ReduceLROnPlateau(verbose=1, min_delta=0.01,
                                    patience=int(patience/2))

        mk_dir("checkpoints")
        model_checkpoint = ModelCheckpoint(
            os.path.join('checkpoints', 'trump_22_01_20.{epoch:02d}-{val_loss:.2f}.hdf5'),
            monitor="val_loss",
            verbose=1,
            save_best_only=True,
            mode="auto",
            save_weights_only=False)

        callbacks = [reduce_lr, early_stop, model_checkpoint]

        # fit model
        history = model.fit(x, y, 
            batch_size=batch_size, 
            epochs=epochs, 
            callbacks=callbacks, 
            shuffle=False, 
            validation_split=0.2)

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
