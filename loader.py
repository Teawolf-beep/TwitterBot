import csv
import re


class Loader:
    @staticmethod
    def open_file(name, delimiter, lines_count, termination_symbol):
        counter = 0
        # Open csv file on the passed path
        with open(name) as csv_file:
            # Get a csv reader with the passed delimiter
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            ret = ''
            # Get an iterator for the csv file (iterates over rows)
            iter_rows = iter(csv_reader)
            next(iter_rows)
            # For each row in the csv file...
            for row in iter_rows:
                # Leave the loop, if the desired number of lines is read already
                if counter == lines_count:
                    break
                # Append the termination symbol to the text and store only the text in a tuple
                ret += row[1] + ' ' + termination_symbol + ' '
                counter += 1

        return ret

    @staticmethod
    def clean_file(doc):
        # Pad punctuation with whitespaces
        doc = re.sub('([.,!?])', r' \1 ', doc)
        # Collapse multiple whitespaces
        doc = re.sub('[ ]{2,}', ' ', doc)
        # Split the string at each whitespace
        tokens = doc.split()

        # Print some information about the size of the input
        print('Total Tokens: %d' % len(tokens))
        print('Unique Tokens: %d' % len(set(tokens)))
        return tokens

    @staticmethod
    def sequence_file(tokens, size):
        # Sequence the data to sequences of the same length
        length = size + 1
        sequences = list()
        # Append all sequences to a list in a loop
        for i in range(length, len(tokens)):
            seq = tokens[i - length:i]
            line = ' '.join(seq)
            sequences.append(line)

        # Print some information about the size of the sequences
        print('Total sequences: {}'.format(len(sequences)))
        return sequences

    @staticmethod
    def store_file(text, filename):
        # Save the whole processed text in a file (not obligatory)
        data = '\n'.join(text)
        file = open(filename, 'w')
        file.write(data)
        file.close()
