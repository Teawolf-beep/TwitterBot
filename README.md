# TwitterBot

The objective of this research project is to design and develop a neural network that is able to create and publish short text messages, further named Tweets, on the social networking service Twitter. The content of these tweets will be based on the tweets of a public personality. Since there is a steady increase of machines and algorithms in our everyday life, researches are looking for ways to facilitate human machine interaction. The most natural way for humans to communicate with other beings is spoken and written language. Therefore, on the one side, it is essential to develop algorithms, which are able to extract information from human language. On the other side it is not less important that these algorithms can form sentences, which are understandable for human beings. In this project we propose a LSTM long short-term memory architecture, that is capable of extracting features with long term dependencies. The prediction will be based on a  starting seed with a word-level approach, so that complete words will be predicted. The data will be scraped from Twitter profiles and can be of arbitrary language. 

## Get a data set

The tweet_dumpre.py script allows to fetch Tweets from a passed username (target). Consequently unwanted content will be removed and the data is written to a csv file.

Please type `python tweet_dumper -h` for information about accepted arguments.

```
usage: tweet_dumper.py [-h] [-s SINCE] [-u UNTIL] [-f FILENAME] [-l LIMIT]
                       [-t TRANSLATOR] [-d DELIMITER] [--overwrite]
                       target

Get Twitter Tweets from the passed target person and stores the attributes of
interest to a csv file.

positional arguments:
  target         The user from which the tweets will be fetched.

optional arguments:
  -h, --help     show this help message and exit
  -s SINCE       A lower bound date to restrict search. "yyyy-mm-dd"
  -u UNTIL       An upper bound date to restrict search. "yyyy-mm-dd". If not
                 passed and a file FILENAME exists in the working directory,
                 the date in the last line will be set as default value.
  -f FILENAME    The filename where the fetched Tweets will be stored. If the
                 file already exists, new Tweets will be appended. Check the
                 --overwrite flag for further information. Default value is
                 "[target]_tweets.csv"
  -l LIMIT       The maximal number of Tweets that will be fetched. Default
                 value is 2000.
  -t TRANSLATOR  A list of characters that will be removed from the Tweets. No
                 separation needed. Default value is ";“”’‘\n\/() .
  -d DELIMITER   The delimiter for the CSV file. Default value is ; .
  --overwrite    Overwrite the given file, if it exists already. Default value
                 is False
```

## Train a model an generate text

Data preparation, training and verification are done via static method calls of the Loader, Trainer and Generator calls. In the twitter_bot.py script is a complete example which should work out of the box. You can alter the Defines on top in order to change parameters.

```
# Defines regarding the csv file
CSV_FILENAME = 'trumpDataset.csv'
CSV_DELIMITER_SYMBOL = ';'
MAX_LINE_COUNT = 5000
TERMINATION_SYMBOL = ';'

# Defines regarding sequencing
SEQUENCE_SIZE = 50
SEQUENCE_FILENAME = 'sequenced_trump_data.txt'

# Defines regarding the training
BATCH_SIZE = 128
EPOCH_COUNT = 100

# Defines regarding model and tokenizer
MODEL_FILENAME = 'trump_5000.h5'
TOKENIZER_FILENAME = 'tokenizer_5000.pkl'

# Defines regarding output generation
MIN_OUTPUT_WORD_COUNT = 10
MAX_OUTPUT_WORD_COUNT = 30


# Open a csv-file
doc = Loader.open_file(CSV_FILENAME, CSV_DELIMITER_SYMBOL, MAX_LINE_COUNT, TERMINATION_SYMBOL)
# # Manipulate the csv-file
tokens = Loader.clean_file(doc)
lines = Loader.sequence_file(tokens, SEQUENCE_SIZE)
# # Save the sequenced and clean data
Loader.store_file(lines, SEQUENCE_FILENAME)
#
# # Alternative: Load prepared file:
# # doc = Trainer.load_file('sequenced_trump_data.txt')
# # lines = doc.split('\n')
#
# # Create a tokenizer and one-hot encode the words
tokenizer, vocab_size = Trainer.tokenize(lines)
# # separate into input and output
x, y, seq_length = Trainer.sequence_data(tokenizer, lines, vocab_size)
# # Build model
model = Trainer.build_model(vocab_size, seq_length)
# # Train the model with a batch size of 128 and 100 epochs (takes a while)
model = Trainer.train_model(x, y, model, BATCH_SIZE, EPOCH_COUNT)

# Save trained model and tokenizer for later usage
Trainer.save_model(model, MODEL_FILENAME)
Trainer.save_tokenizer(tokenizer, TOKENIZER_FILENAME)


# Second step: Generate Tweets with the trained model

# # Open the sequenced data (if not open already)
# doc = Trainer.load_file(SEQUENCE_FILENAME)
# lines = doc.split('\n')
# # Make all letters lower case
# lines = [word.lower() for word in lines]

# Get sequence length (50 in this case)
seq_length = len(lines[0].split()) - 1

# Load model and tokenizer
model = Generator.load_trained_model(MODEL_FILENAME)
tokenizer = Generator.load_tokenizer(TOKENIZER_FILENAME)

# Select and print a random seed text (we can make up our own seed text as well,
# better results are expected with this approach tho. The tokenizer ignores word that are not known to him)
seed_text = lines[randint(0, len(lines))]
print(seed_text + '\n')

# Generate and print a sequence with a word length of minimum 10 and maximum 30
generated = Generator.generate_seq(model, tokenizer, seq_length, seed_text, MIN_OUTPUT_WORD_COUNT, MAX_OUTPUT_WORD_COUNT)
# Post-process and print generated text
print(Generator.postprocess(generated))
```
  
