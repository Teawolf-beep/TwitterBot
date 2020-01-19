from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
import random
import os
import pandas as pd
import time
import tensorflow as tf


class Tweetdataset:
    def get_text(self, maxlen=40, step=1, future_target=1):
        '''path_to_file = tf.keras.utils.get_file(
            origin='https://www.kaggle.com/kingburrito666/better-donald-trump-tweets/download',
            fname='better-donald-trump-tweets.zip',
            extract=True)
        csv_path, _ = os.path.splitext(path_to_file)'''



        # read dataframe from csv file
        df = pd.read_csv('dataset/Donald-Tweets!.csv')
        # print the head of dataset
        print(df.shape)
        print(df.head())

        # clean and gain some info about the dataset
        text = df["Tweet_Text"].str.lower()

        print("Before:")
        print(text[0])
        text = text.map(lambda s: ' '.join([x for x in s.split() if 'http' not in x]))
        print("After:")
        print(text[0])

        print('max tweet len:',text.map(len).max())
        print('min tweet len:',text.map(len).min())
        print(text.map(len).hist())

        print(len(text))
        text = text[text.map(len)>60]
        print(len(text))

        chars = sorted(list(set(''.join(text))))
        print('total chars:', len(chars))
        print(chars)
        char_indices = dict((c, i) for i, c in enumerate(chars))
        indices_char = dict((i, c) for i, c in enumerate(chars))

        #
        for c in chars[-19:]:
            print("\nCHAR: ", c)
            smple = [x for x in text if c in x]
            print(random.sample(smple,min(3,len(smple))))
            text = text.str.replace(c, "")

        # sort the whole dataset
        chars = sorted(list(set(''.join(text))))
        print('total chars:', len(chars))
        char_indices = dict((c, i) for i, c in enumerate(chars))
        indices_char = dict((i, c) for i, c in enumerate(chars))


        sentences = []
        next_chars = []

        #
        for x in text:
            for i in range(0, len(x) - maxlen, step):
                sentences.append(x[i: i + maxlen])
                next_chars.append(x[i + maxlen])
        print("nb sequences: ", len(sentences))

        # vectorization the dataset
        print('Vectorization...')
        x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
        y = np.zeros((len(sentences), len(chars)), dtype=np.bool)

        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                x[i, t, char_indices[char]] = 1
            y[i, char_indices[next_chars[i]]] = 1
        print("X: ")
        print(x)
        print("Y: ")
        print(y)

        character=len(chars)
        return text, x, y, character, char_indices, indices_char
