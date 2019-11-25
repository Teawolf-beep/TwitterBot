from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
from keras.optimizers import Adam


class MultiStepLSTM:
    def get_model(self, input_shape, summary=True, future_target=1):
        tweet_generator_model = Sequential()
        tweet_generator_model.add(LSTM(128, input_shape=input_shape, return_sequences=True))
        tweet_generator_model.add(Dropout(0.5))
        tweet_generator_model.add(LSTM(128, return_sequences=True, activation='relu'))
        tweet_generator_model.add(LSTM(128, return_sequences=True, activation='relu'))
        tweet_generator_model.add(Dropout(0.5))
        tweet_generator_model.add(Dense(input_shape[0]), activation='softmax')

        # optimizer = RMSprop(lr=0.01)
        optimizer = Adam()
        tweet_generator_model.compile(loss='categorical_crossentropy', optimizer=optimizer)

        if summary:
            tweet_generator_model.summary()
        return tweet_generator_model