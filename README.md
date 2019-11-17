# TwitterBot

Github erlaubt nur 100MB im Repository, wir laden also nur den Code usw hoch und jeder verwaltet virtualenv, conda, whatever selbst.

## Install
Um get_tweets.py zu benutzen, müsst ihr GetOldTweets3 (pip install GetOldTweets3) installieren.

## Usage
Virtualenv sourcen (wenn ihr ohne Anaconda seid) und python get_tweets.py -h für Hilfe.

### Example
```
python get_tweets.py realDonaldTrump 
```

Wenn ihr den Befehl mehrmals hintereinander ausführt, wird automatisch das letzte Datum der csv-Datei als limit genommen (es werden nur ältere Tweets geholt). Wenn ihr neu anfangen wollt --overwrite flag setzen.
