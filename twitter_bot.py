from random import randint

from loader import Loader
from trainer import Trainer
from generator import Generator

# # Open csv-file
# doc = Loader.open_file('trumpDataset.csv', ';', 5000, ';')
# # Manipulate the csv-file
# tokens = Loader.clean_file(doc)
# lines = Loader.sequence_file(tokens, 50)
# # Save the sequenced and clean data
# Loader.store_file(lines, 'sequenced_trump_data.txt')
#
#Alternative: Load prepared file:
doc = Trainer.load_file('sequenced_trump_data.txt')
lines = doc.split('\n')
#
# # Create a tokenizer and one-hot encode the words
tokenizer, vocab_size = Trainer.tokenize(lines)
# # separate into input and output
x, y, seq_length = Trainer.sequence_data(tokenizer, lines, vocab_size)
# # Build model(two LSTM hidden layer with 100 neurons,
# # a dense fully connected layer with 100 neurons (relu), output layer (softmax)
model = Trainer.build_model(vocab_size, seq_length)
# # Train the model with a batch size of 128 and 150 epochs (takes a while)
model = Trainer.train_model(x, y, model, 128, 50)

# Save trained model and tokenizer for later usage
Trainer.save_model(model, 'trump_5000.h5')
Trainer.save_tokenizer(tokenizer, 'tokenizer_5000.pkl')

# Second step: Generate Tweets with the trained model
# Open the sequenced data (if not open already)
doc = Trainer.load_file('sequenced_trump_data.txt')
lines = doc.split('\n')
# Make all letters lower case
lines = [word.lower() for word in lines]

# Get sequence length (50 in this case)
seq_length = len(lines[0].split()) - 1

# Load model and tokenizer
model = Generator.load_trained_model('trump_5000.h5')
tokenizer = Generator.load_tokenizer('tokenizer_5000.pkl')

# Select and print a random seed text (we can make up our own seed text as well,
# better results are expected with this approach tho. The tokenizer ignores word that are not known to him)
seed_text = 'hello america i am trump'#  lines[randint(0, len(lines))]
print(seed_text + '\n')

# Generate and print a sequence with a word length of 30
generated = Generator.generate_seq(model, tokenizer, seq_length, seed_text, 10)
print(Generator.postprocess(generated))


