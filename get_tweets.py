<<<<<<< HEAD
import GetOldTweets3 as got
import csv
import argparse
import signal
import os
import re
=======
import argparse
import tweepy
import csv
import re
import signal
import sys

"""
Type 'python get_tweets -h' for help!

Tweepy uses old names since the names of Twitter concepts have changed over time:
status      = Tweet
friendship  = follow-follower relationship
favorite    = like
"""

# Credentials for authentication
CONSUMER_KEY = "WLSWVvjArQOYjr8ajgynKPh9z"
CONSUMER_SECRET = "yp7iRWbsdHj0sDcQVomOEzugGJ3MslFhokE0cnCXTkGW7x2w3e"
ACCESS_TOKEN = "1187027821224480769-X0TZPT5qirpkMn7SfF3Jh5HA8rwDUu"
ACCESS_TOKEN_SECRET = "6TF4uQdZxFu123ijVNIPVzFvUSkIW0bAXjEKM4vQWWl9d"

# Global variable running (needed for signal handler)
running = True


def signal_handler(signal_number, frame):
    print("Signal received: " + str(signal_number) + "\nStop fetching Tweets")
    global running
    running = False
>>>>>>> Initial commit


def add_filename(args):
    # Get filename (create it, if not passed)
    if args.filename == '_tweets.csv':
        args.filename = args.target + args.filename

    return args


def get_arguments():
<<<<<<< HEAD
    # Define command-line description
=======
    # Define Command-line description
>>>>>>> Initial commit
    parser = argparse.ArgumentParser(description='Get Twitter Tweets from the passed target '
                                                 'person and store the attributes of interest to a CSV file.')
    # Define command-line argument "target"
    parser.add_argument('target', type=str,
                        help='The user from which the tweets will be fetched.')

<<<<<<< HEAD
    # Define command-line argument "since"
    parser.add_argument('-s', dest='since', type=str,
                        help='A lower bound date to restrict search. "yyyy-mm-dd"')

    # Define command-line argument "until"
    parser.add_argument('-u', dest='until', type=str,
                        help='An upper bound date to restrict search. "yyyy-mm-dd"')
=======
    # Define command-line argument "attributes"
    parser.add_argument('-a', type=str, dest='attributes', nargs='+',
                        default=['created_at', 'id_str', 'full_text', 'retweet_count', 'favorite_count'],
                        help='The attributes of the Tweets that will be stored in the output file. '
                        'Please enter the wished attributes of interest separated by spaces. '
                        'If no attributes are passed, default values will be stored. The default values are: '
                        'created_at, id_str, full_text, retweet_count, favorite_count; '
                        'For further information please visit: '
                        'https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object')
>>>>>>> Initial commit

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
<<<<<<< HEAD
    parser.add_argument('-t', type=str, dest='translator', default='\';“”’‘"\n',
                        help='A list of characters that will be removed from the Tweets. No separation needed. '
                             'If not passed, \";“”’‘\\n will be removed by default.')
=======
    parser.add_argument('-t', type=str, dest='translator', default='\"$%%&\'()*+-/:;<=>[\\]^_`{|}~“”’‘\n',
                        help='A list of characters that will be removed from the Tweets. No separation needed. '
                             'If not passed, \"$%%&\'()*+-/:;<=>[\\]^_`{|}~“”’‘\\n will be removed by default.')

    # Define command-line argument "id"
    parser.add_argument('-i', type=int, dest='target_id', default=sys.maxsize,
                        help='The target ID. Only Tweets with an older ID will be fetched.'
                             'If not passed, the newest available ID will be used instead.')
>>>>>>> Initial commit

    # Define command-line argument "delimiter
    parser.add_argument('-d', type=str, dest='delimiter', default=';',
                        help='The delimiter for the CSV file. If not passed, the default delimiter (;) will be used.')

<<<<<<< HEAD
=======
    # Define command-line argument "force"
    parser.add_argument('--force', action='store_const', const=True, default=False,
                        help='Force to fetch all Tweets until the limit.')

>>>>>>> Initial commit
    # Define command-line argument "overwrite"
    parser.add_argument('--overwrite', action='store_const', const=True, default=False,
                        help='Overwrite the given file, if it exists already')

    # Get command-line arguments
    arguments = parser.parse_args()
    # Get the correct filename and return everything
    return add_filename(arguments)


class TweetDumper:
    def __init__(self, args):
<<<<<<< HEAD
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
=======
        # Get target
        self.target = args.target

        # Get attributes (cannot be empty)
        self.attributes = args.attributes

        # Define further member variables
        self.api = None
        self.content = []
        self.content.append(self.attributes)
        self.translator = str.maketrans('', '', args.translator)

    def initialize(self, consumer_key, consumer_secret, access_token, access_token_secret):
        # Authenticate Twitter app
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        # Create an API object
        self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        print("Getting data of " + self.target + "...")

        # Get user object
        person = self.api.get_user(self.target)

        # Print some user information
        print("Name: " + person.name)
        print("Description: " + person.description)
        print("Location: " + person.location)
        print("Follower count: " + str(person.followers_count))
        print("Tweet count: " + str(person.statuses_count))

    def fetch_tweets(self, limit, target_id, force):
        # Get the first batch of Tweets (maximum count is 200)
        fetched_tweets = self.api.user_timeline(screen_name=self.target, tweet_mode='extended',
                                                count=(limit if (limit < 200) else 200), max_id=target_id)

        # Store the attributes of interest of the fetched Tweets
        for t in fetched_tweets:
            self.store_tweet(t)

        # Calculate how many Tweets remain
        remaining_tweets = limit - len(fetched_tweets)
        while (remaining_tweets > 0) and ((len(fetched_tweets) > 0) if (force is False) else True) and (
                running is True):
            # Get the ID of the oldest Tweet minus 1
            if len(fetched_tweets) > 0:
                target_id = fetched_tweets[-1].id - 1

            # Fetch as many Tweets as possible or wanted
            fetched_tweets = self.api.user_timeline(
                screen_name=self.target, tweet_mode='extended',
                count=(remaining_tweets if (remaining_tweets < 200) else 200), max_id=target_id)

            # Store the attributes of interest of the fetched Tweets
            for t in fetched_tweets:
                self.store_tweet(t)

            # Figure out how many Tweets are missing
            remaining_tweets = limit - len(self.content) + 1

            # Print information about the progress
            print("{} Tweets fetched so far, {} Tweets remaining...".format(len(self.content) - 1, remaining_tweets))

    def store_tweet(self, tweet):
        # True, if the Tweet is originally of the target person (not a retweet) and the full_text attribute is not empty
        if (not hasattr(tweet, 'retweeted_status')) and tweet.full_text:
            row = []
            for attribute in self.attributes:
                # Get all attributes of interest, remove punctuation as well as links (everything beginning with http)
                row.append(re.sub(r"\bhttp\w+", "", str(getattr(tweet, attribute, "NP")).translate(self.translator)))
            # Safe the Tweet in a buffer
            self.content.append(row)

    def store_data(self, filename, delimiter, overwrite):
        with open(filename, 'w' if overwrite else 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter=delimiter)
            writer.writerows(self.content)

        csv_file.close()
        print("Wrote {0} Tweets to ".format(len(self.content) - 1) + filename)
>>>>>>> Initial commit


def main():
    args = get_arguments()
    tweet_dumper = TweetDumper(args)
<<<<<<< HEAD
    tweet_dumper.get_tweets()


if __name__ == '__main__':
=======
    tweet_dumper.initialize(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    tweet_dumper.fetch_tweets(args.limit, args.target_id - 1, args.force)
    tweet_dumper.store_data(args.filename, args.delimiter, args.overwrite)


if __name__ == '__main__':
    # Register signals to be caught by the signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

>>>>>>> Initial commit
    # Run main()
    main()
