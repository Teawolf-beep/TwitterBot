# utils for plotting
from keras.callbacks import LambdaCallback, ModelCheckpoint,ReduceLROnPlateau, EarlyStopping
from keras.callbacks import TensorBoard
import matplotlib.pyplot as plt
import random
import sys
import logging
import io
import os
import pandas as pd
from utils import mk_dir
from Sources.plt import show_plot, multi_step_plot
import numpy as np
logging.basicConfig(level=logging.DEBUG)
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
        patience = 4        

        FINAL_WEIGHTS_PATH = 'final_weights.hdf5'

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

        epochs = 5

        #model callback
        early_stop = EarlyStopping('loss', patience=patience)
        reduce_lr = ReduceLROnPlateau(verbose=1, epsilon=0.001,
                                     patience=int(patience/2))

        mk_dir("checkpoints")
        model_checkpoint =[ModelCheckpoint(
            os.path.join('checkpoints', 'weights.{epoch:02d}-{loss:.4f}.hdf5'),
            monitor='loss',
            verbose=1,
            save_best_only=True,
            mode="min")]

        #callbacks = [model_checkpoint]
        #callbacks = LambdaCallback(model_checkpoint, on_epoch_end=on_epoch_end,
        #                          early_stop, reduce_lr)

        hist = model.fit(x, y,
                 batch_size=128,
                 epochs=epochs,
                 verbose=1,
                 callbacks=model_checkpoint)

      
        mk_dir("trained_models")
        logging.debug("Saving weights...")
        model.save(os.path.join("trained_models", "MobileNet_model.h5"))
        model.save_weights(os.path.join("trained_models", FINAL_WEIGHTS_PATH), overwrite=True)
        pd.DataFrame(hist.history).to_hdf(os.path.join("trained_models", "history.h5"), "history")

        logging.debug("plot the results...")
        input_path = "trained_models/history.h5"
        df = pd.read_hdf(input_path, "history")
        input_dir = os.path.dirname(input_path) 
        plt.plot(df["loss"], label="loss (gender)")
        #plt.plot(df["age_loss"], label="loss (age)")
        plt.plot(df["val_loss"], label="val_loss")
        #plt.plot(df["val_age_loss"], label="val_loss (age)")
        plt.xlabel("number of epochs")
        plt.ylabel("loss")
        plt.legend()
        plt.savefig(os.path.join(input_dir, "loss.png"))
        plt.cla()

        plt.plot(df["acc"], label="accuracy (gender)")
        #plt.plot(df["age_acc"], label="accuracy (age)")
        plt.plot(df["val_acc"], label="val_accuracy")
        #plt.plot(df["val_age_acc"], label="val_accuracy (age)")
        plt.xlabel("number of epochs")
        plt.ylabel("accuracy")
        plt.legend()
        plt.savefig(os.path.join(input_dir, "accuracy.png"))


            

