# TwitterBot

Github erlaubt nur 100MB im Repository, wir laden also nur den Code usw hoch und jeder verwaltet virtualenv, conda, whatever selbst.
Um das Skript zu benutzen, müsst ihr tweepy (pip install tweepy) installieren.

## Usage

python get_tweets.py -h gibt Hilfe zu allen command-line arguments, die das Skript versteht. Das ist die Ausgabe:
usage: get_tweets.py [-h] [-a ATTRIBUTES [ATTRIBUTES ...]] [-f FILENAME]
                     [-l LIMIT] [-t TRANSLATOR] [-i TARGET_ID] [-d DELIMITER]
                     [--force] [--overwrite]
                     target

Get Twitter Tweets from the passed target person and store the attributes of
interest to a CSV file.

positional arguments:
  target                The user from which the tweets will be fetched.

optional arguments:
  -h, --help            show this help message and exit
  -a ATTRIBUTES [ATTRIBUTES ...]
                        The attributes of the Tweets that will be stored in
                        the output file. Please enter the wished attributes of
                        interest separated by spaces. If no attributes are
                        passed, default values will be stored. The default
                        values are: created_at, id_str, full_text,
                        retweet_count, favorite_count; For further information
                        please visit:
                        https://developer.twitter.com/en/docs/tweets/data-
                        dictionary/overview/tweet-object
  -f FILENAME           The filename where the fetched Tweets will be stored.
                        If the file already exists,new Tweets will be
                        appended. Check the --overwrite flag for further
                        informationIf not passed, the output file will be
                        called "[target]_tweets.csv"
  -l LIMIT              The maximal number of Tweets that will be fetched. If
                        not passed, 2000 Tweets will be fetched.
  -t TRANSLATOR         A list of characters that will be removed from the
                        Tweets. No separation needed. If not passed,
                        "$%&'()*+-/:;<=>[\]^_`{|}~“”’‘\n will be removed by
                        default.
  -i TARGET_ID          The target ID. Only Tweets with an older ID will be
                        fetched.If not passed, the newest available ID will be
                        used instead.
  -d DELIMITER          The delimiter for the CSV file. If not passed, the
                        default delimiter (;) will be used.
  --force               Force to fetch all Tweets until the limit.
  --overwrite           Overwrite the given file, if it exists already
  
  ## Take care
  
  Das Limit liegt default bei 2000, mehr gibt die API in einem Aufruf eh nicht her. Wollt ihr mehr Tweets haben, 
  müsst ihr den letzten Identifier kopieren und das Skript mit der -i Option aufrufen. Ist der Name der Datei der gleiche,
  werden die neuen Tweets default ans Ende angehängt. Wenn die --overwrite flag gesetzt ist, wird die Datei überschrieben.
  Ich würde immer die --force flag setzen (sollen wir das als default nehmen??), weil der sonst eine beliebige Anzahl Tweets
  holt. Mit dem default Translator werden nur #.,@ übernommen. Andere Sonderzeichen (Außer Emojis) werden entfernt.
  
  Beispiel: python get_tweets.py -f tweets.csv -l 500 -i 1189592785311223815 --force
  
  Holt 500 Tweets, die eine ID vor 1189592785311223815 haben und speichert sie in tweets.csv. Existiert die Datei,
  werden die Tweets angehängt, existiert sie nicht, wird eine neue Datei erstellt.
  
  ## Get limit
  
  Wenn ihr mehrere Tweets holen wollt, lasst dazwischen immer eine Pause von ca. ner halben Stunde und übertreibt nicht,
  keine Anhnug, ab wann die uns den Account sperren...
  
  ## Viel Spaß Kinder!
  
