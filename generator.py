from pickle import load
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


class Generator:
    @staticmethod
    def generate_seq(model, tokenizer, seq_length, seed, word_count):
        result = list()
        in_text = seed
        for _ in range(word_count):
            # Encode the text as integer
            encoded = tokenizer.texts_to_sequences([in_text])[0]
            # Truncate sequences to a fixed length
            encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
            # Predict probabilities for each word
            yhat = model.predict_classes(encoded, verbose=0)
            out_word = ''
            for word, index in tokenizer.word_index.items():
                if index == yhat:
                    out_word = word
                    break

            in_text += ' ' + out_word
            result.append(out_word)
        return ' '.join(result)

    @staticmethod
    def load_trained_model(filename):
        return load_model(filename)

    @staticmethod
    def load_tokenizer(filename):
        return load(open(filename, 'rb'))
