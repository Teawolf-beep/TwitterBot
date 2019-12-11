from numpy import array
from pickle import dump
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Embedding

from loader import Loader

doc = Loader.open_file('trumpDataset.csv', ';')
tokens = Loader.clean_file(doc)
lines = Loader.sequence_file(tokens, 50)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(lines)
sequences = tokenizer.texts_to_sequences(lines)

# vocabulary size
vocab_size = len(tokenizer.word_index) + 1

sequences = array(sequences)
print(sequences.shape)
X, y = sequences[:, :-1], sequences[:, -1]
# y = to_categorical(y, num_classes=vocab_size)
# seq_length = X.shape[1]

# model = Sequential()
# model.add(Embedding(vocab_size, 50, input_length=seq_length))
# model.add(LSTM(100, return_sequences=True))
# model.add(LSTM(100))
# model.add(Dense(100, activation='relu'))
# model.add(Dense(vocab_size, activation='softmax'))
# print(model.summary())
#
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# # fit model
# model.fit(X, y, batch_size=128, epochs=100)
#
# # save the model to file
# model.save('model.h5')
# # save the tokenizer
# dump(tokenizer, open('tokenizer.pkl', 'wb'))
