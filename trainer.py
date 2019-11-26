# utils for plotting
from keras.callbacks import LambdaCallback
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt
import random
import sys
import io
from Sources.plt import show_plot, multi_step_plot
import numpy as np
# models
from model.lstm_model import MultiStepLSTM as Mdl
# datasets
from dataset.tweets import Tweetdataset as Dataset

class Trainer:
    def __init__(self, config):
        self.batch_size = config.batch_size
        self.epochs = config.epochs
        self.maxlen=config.maxlen
        self.future_target=config.future_target
        self.data = Dataset()
        self.mdl = Mdl()

    def train(self, plot=True):
        future_target = 128
        maxlen = 40
        step = 1

        text, x, y, character, char_indices, indices_char= self.data.get_text(self.maxlen)

        model = self.mdl.get_model( self.maxlen, character)

        def sample(preds, temperature=1.0):
            # helper function to sample an index from a probability array
            preds = np.asarray(preds).astype('float64')
            preds = np.log(preds) / temperature
            exp_preds = np.exp(preds)
            preds = exp_preds / np.sum(exp_preds)
            probas = np.random.multinomial(1, preds, 1)
            return np.argmax(probas)

        def on_epoch_end(epoch, _):
            # Function invoked at end of each epoch. Prints generated text.
            print()
            print('----- Generating text after Epoch: %d' % epoch)

            #     start_index = random.randint(0, len(text) - maxlen - 1)
            tweet = np.random.choice(text)  # select random tweet
            start_index = 0

            for diversity in [0.2, 0.5, 1.0, 1.2]:
                print('----- diversity:', diversity)

                generated = ''
                sentence = tweet[start_index: start_index + self.maxlen]
                generated += sentence
                print('----- Generating with seed: "' + sentence + '"')
                sys.stdout.write(generated)

                for i in range(120):
                    x_pred = np.zeros((1, self.maxlen, character))
                    for t, char in enumerate(sentence):
                        x_pred[0, t, char_indices[char]] = 1.

                    preds = model.predict(x_pred, verbose=0)[0]
                    next_index = sample(preds, diversity)
                    next_char = indices_char[next_index]

                    generated += next_char
                    sentence = sentence[1:] + next_char

                    sys.stdout.write(next_char)
                    sys.stdout.flush()
                print()

        epochs = 20

        print_callback = LambdaCallback(on_epoch_end=on_epoch_end)

        model.fit(x, y,
                 batch_size=128,
                 epochs=epochs,
                 callbacks=[print_callback])