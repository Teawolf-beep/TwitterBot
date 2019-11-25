from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.optimizers import Adam
import tensorflow as tf





class MultiStepLSTM:
    tf.keras.backend.clear_session()  # For easy reset of notebook state.
    def get_model(self, maxlen, character, summary=True, future_target=1):
        tweet_generator_model = Sequential()
        tweet_generator_model.add(LSTM(128, input_shape=(maxlen, character), return_sequences=True))
        tweet_generator_model.add(Dropout(0.5))
        tweet_generator_model.add(LSTM(128, return_sequences=True, activation='relu'))
        tweet_generator_model.add(LSTM(128, activation='relu'))
        tweet_generator_model.add(Dropout(0.5))
        tweet_generator_model.add(Dense(character, activation='softmax'))   
        # optimizer = RMSprop(lr=0.01)
        optimizer = Adam()
        tweet_generator_model.compile(loss='categorical_crossentropy', optimizer=optimizer)

        if summary:
            tweet_generator_model.summary()
        return tweet_generator_model