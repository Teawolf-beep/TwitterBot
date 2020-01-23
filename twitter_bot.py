from random import randint

from loader import Loader
from trainer import Trainer
from generator import Generator

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


