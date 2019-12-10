# TwitterBot

Github erlaubt nur 100MB im Repository, wir laden also nur den Code usw hoch und jeder verwaltet virtualenv, conda, whatever selbst.

## Install
Um get_tweets.py zu benutzen, müsst ihr GetOldTweets3 (pip install GetOldTweets3) installieren.
um die Vorausetzungen zu erfüllen :
pip install -r requirements.txt
python pre_processing/requirements_installer.py
## Usage
Virtualenv sourcen (wenn ihr ohne Anaconda seid) und python get_tweets.py -h für Hilfe.

Pre-processor :

The list of methods that can currently be used are:

    remove_urls - Removes all urls (e.g. 'https://ptwist.eu')
    remove_mentions - Removes all mentions (e.g. '@PlasticTwistBot')
    remove_hashtags - Removes all hashtags (e.g. '#plastictwist')
    remove_twitter_reserved_words - Removes Twitter reserved words (e.g. 'RT', 'via')
    remove_punctuation - Removes punctuation (e.g. '.', '!')
    remove_single_letter_words - Removes single-letter words (e.g. 'b', 'f')
    remove_blank_spaces - Removes blank spaces
    remove_stopwords - Removes stopwords (e.g. 'a', 'at', 'here')
        has an extra_stopwords parameter (list) that allows users to add extra stopwords
    remove_profane_words - Removes profane words
    remove_numbers - Removes numbers (e.g. '2', '999')
        has an preserve_years parameter (boolean) that allows users to choose whether or not years should be removed.

Ihr könnte auswählen,ob agnzen method or nur einige davon aufgeruft werden sollen
### Example
```
python get_tweets.py realDonaldTrump 
```

Wenn ihr den Befehl mehrmals hintereinander ausführt, wird automatisch das letzte Datum der csv-Datei als limit genommen (es werden nur ältere Tweets geholt). Wenn ihr neu anfangen wollt --overwrite flag setzen.
