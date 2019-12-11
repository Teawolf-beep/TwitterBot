import csv
import string
import re


class Loader:
    @staticmethod
    def open_file(name, delimiter, lines, termination):
        counter = 0
        with open(name) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=delimiter)
            ret = ''
            iter_rows = iter(csv_reader)
            next(iter_rows)
            for row in iter_rows:
                if counter == lines:
                    break
                ret += row[1] + ' ' + termination + ' '
                counter += 1

        return ret

    @staticmethod
    def clean_file(doc):
        # Pad punctuation with whitespaces
        doc = re.sub('([.,!?():#])', r' \1 ', doc)
        # Collapse multiple whitespaces
        doc = re.sub('[ ]{2,}', ' ', doc)
        # Split the string at each whitespace
        tokens = doc.split()

        # Transform all letters to lowercase
        # tokens = [word.lower() for word in tokens]
        print('Total Tokens: %d' % len(tokens))
        print('Unique Tokens: %d' % len(set(tokens)))
        return tokens

    @staticmethod
    def sequence_file(tokens, size):
        length = size + 1
        sequences = list()
        for i in range(length, len(tokens)):
            seq = tokens[i - length:i]
            line = ' '.join(seq)
            sequences.append(line)

        print('Total sequences: {}'.format(len(sequences)))
        return sequences

    @staticmethod
    def store_file(text, filename):
        data = '\n'.join(text)
        file = open(filename, 'w')
        file.write(data)
        file.close()
