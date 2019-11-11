import numpy as np
import random
import os
import pandas as pd
from io import BytesIO
from urllib.request import urlopen
from zipfile import ZipFile
import tensorflow as tf
...

# pass the root url to save our dataset in it
from Sources.utils import get_project_root

root = get_project_root()


class Tweetsdataset:
    def get_text(self, debug=True, plot=True, future_target=128):
        ...
        '''
        # download and save dataset at the same path
        zipurl = 'https://storage.googleapis.com/kaggle-data-sets/1121/2025/bundle/archive.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1573684932&Signature=lPl1qhhNHYj5n33W05Y933BWevkrmlKTS1wM6bFECzYhDVg%2BVObL1rThaB48HOIvDsHkFyROghlEIq8mINWvsZCYJFCKCjcf90P4A0u9n5zsHRQTQCGE4xL37ZjDbXU33Ax15P7KV4USiqOfk71Ys4rLfvoIkSKNG31wr3WKytOKzGxKeDZEvXXqelUsDdCkKWlqEgYx18CvVsH27vUF%2BKyCxhbOW5c71C5%2BgrIDezayOCdb8ra3jppKJR3ZNVTdOZiP2lD9jZEs%2BaqbF1dgLFg9sLRyaZmGI%2BfN2X663jSfDd7wB5lhUDlenX7S6Db98Yun1fmp1ReBUgJ9GCqYkw%3D%3D&response-content-disposition=attachment%3B+filename%3Dbetter-donald-trump-tweets.zip'
        with urlopen(zipurl) as zipresp:
            with ZipFile(BytesIO(zipresp.read())) as zfile:
                zfile.extractall('./')
        '''
        zip_path = tf.keras.utils.get_file(
            origin='https://storage.googleapis.com/kaggle-data-sets/1121/2025/bundle/archive.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1573684932&Signature=lPl1qhhNHYj5n33W05Y933BWevkrmlKTS1wM6bFECzYhDVg%2BVObL1rThaB48HOIvDsHkFyROghlEIq8mINWvsZCYJFCKCjcf90P4A0u9n5zsHRQTQCGE4xL37ZjDbXU33Ax15P7KV4USiqOfk71Ys4rLfvoIkSKNG31wr3WKytOKzGxKeDZEvXXqelUsDdCkKWlqEgYx18CvVsH27vUF%2BKyCxhbOW5c71C5%2BgrIDezayOCdb8ra3jppKJR3ZNVTdOZiP2lD9jZEs%2BaqbF1dgLFg9sLRyaZmGI%2BfN2X663jSfDd7wB5lhUDlenX7S6Db98Yun1fmp1ReBUgJ9GCqYkw%3D%3D&response-content-disposition=attachment%3B+filename%3Dbetter-donald-trump-tweets.zip',
            fname='jena_climate_2009_2016.csv.zip',
            extract=True)
        csv_path, _ = os.path.splitext(zip_path)
        ...
        # reasd dataframe from csv file
        df = pd.read_csv("./Donald-Tweets!.csv")
        # print the head of dataset
        print(df.shape)
        print(df.head())

        ...
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

        maxlen = 40
        step = 1
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

        train_data = x
        val_data = y
        ...
        return train_data, val_data, text,  (maxlen,len(chars))