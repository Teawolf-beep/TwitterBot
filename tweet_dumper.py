import GetOldTweets3 as got
import csv
import argparse
import os
import re


def add_filename(args):
    # Get filename (create it, if not passed)
    if args.filename == '_tweets.csv':
        args.filename = args.target + args.filename

    return args


def get_arguments():
    # Define command-line description
    parser = argparse.ArgumentParser(description='Get Twitter Tweets from the passed target '
                                                 'person and store the attributes of interest to a CSV file.')
    # Define command-line argument "target"
    parser.add_argument('target', type=str,
                        help='The user from which the tweets will be fetched.')

    # Define command-line argument "since"
    parser.add_argument('-s', dest='since', type=str,
                        help='A lower bound date to restrict search. "yyyy-mm-dd"')

    # Define command-line argument "until"
    parser.add_argument('-u', dest='until', type=str,
                        help='An upper bound date to restrict search. "yyyy-mm-dd"')

    # Define command-line argument "filename"
    parser.add_argument('-f', type=str,  dest='filename', default='_tweets.csv',
                        help='The filename where the fetched Tweets will be stored. If the file already exists,'
                        'new Tweets will be appended. Check the --overwrite flag for further information'
                        'If not passed, the output file will be called "[target]_tweets.csv"')

    # Define command-line argument "limit"
    parser.add_argument('-l', type=int, dest='limit', default=2000,
                        help='The maximal number of Tweets that will be fetched. '
                        'If not passed, 2000 Tweets will be fetched.')

    # Define command-line argument "translator" (watch out for characters that have to be escaped!!)
    parser.add_argument('-t', type=str, dest='translator', default='\';“”’‘"\n\\/()',
                        help='A list of characters that will be removed from the Tweets. No separation needed. '
                             'If not passed, \";“”’‘\\n\\/() will be removed by default.')

    # Define command-line argument "delimiter
    parser.add_argument('-d', type=str, dest='delimiter', default=';',
                        help='The delimiter for the CSV file. If not passed, the default delimiter (;) will be used.')

    # Define command-line argument "overwrite"
    parser.add_argument('--overwrite', action='store_const', const=True, default=False,
                        help='Overwrite the given file, if it exists already')

    # Get command-line arguments
    arguments = parser.parse_args()
    # Get the correct filename and return everything
    return add_filename(arguments)


class TweetDumper:
    def __init__(self, args):
        # Copy command-line arguments
        self.filename = args.filename
        self.translator = str.maketrans('', '', args.translator)
        self.delimiter = args.delimiter
        self.overwrite = args.overwrite

        if not os.path.isfile(self.filename) or self.overwrite:
            self.make_new_file = True
        else:
            self.make_new_file = False

        # Create TweetCriteria object
        self.tweet_criteria = got.manager.TweetCriteria()

        # Set mandatory TweetCriteria arguments
        self.tweet_criteria.setUsername(args.target)
        self.tweet_criteria.setMaxTweets(args.limit)

        # Set optional TweetCriteria arguments
        if args.since:
            self.tweet_criteria.setSince(args.since)

        if args.until:
            self.tweet_criteria.setUntil(args.until)
        elif not self.make_new_file:
            self.tweet_criteria.setUntil(self.get_until_from_file())

    def get_until_from_file(self):
        with open(self.filename, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.delimiter)
            return list(csv_reader)[-1][0].partition(' ')[0]

    def get_tweets(self):
        rows = []
        if self.make_new_file:
            rows.append(['date', 'text'])

        for tweet in got.manager.TweetManager.getTweets(self.tweet_criteria):
            processed_text = self.preprocess_text(tweet.text)
            if processed_text:
                rows.append([tweet.date.strftime('%Y-%m-%d %H:%M:%S'), processed_text + ';'])

        with open(self.filename, 'w' if self.make_new_file else 'a') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=self.delimiter,
                                    escapechar=self.delimiter, quoting=csv.QUOTE_NONE)
            csv_writer.writerows(rows)

        print("Wrote {} Tweets to ".format(len(rows)) + self.filename)

    def preprocess_text(self, text):
        # Remove links (everything beginning with http)
        text = re.sub(r'http\S+', '', text)
        # Remove retweets (everything beginning with .co)
        text = re.sub(r't.co\S+', '', text)
        # Remove picture or video links (everything with pic.twitter)
        text = re.sub(r'pic.twitter\S+', '', text)
        # Remove multiple dots in the Tweets
        text = re.sub(r'(\.){2,}', '', text)
        # Remove weird dots in the Tweets (those are not 3 dots! Char number 8230)
        text = re.sub(r'…', '', text)
        # Remove the characters specified by the translator and tailing whitespace
        return text.translate(self.translator).rstrip()


def main():
    args = get_arguments()
    tweet_dumper = TweetDumper(args)
    tweet_dumper.get_tweets()


if __name__ == '__main__':
    # Run main()
    main()
