import csv
import nltk
from nltk.stem.porter import *
from nltk.corpus import stopwords
from datetime import datetime

inicio = datetime.now()

def quitarStop(tweet):
    nuevo_tweet = list()
    tweet = tweet.strip().split(' ')
    for palabra in tweet:
        if palabra in stop_words: continue
        else: nuevo_tweet.append(palabra)
    nuevo_tweet = ' '.join(nuevo_tweet)
    return nuevo_tweet

def stemming(tweet):
    nuevo_tweet = list()
    tweet = tweet.strip().split(' ')
    for palabra in tweet:
        palabra = ps.stem(palabra)
        nuevo_tweet.append(palabra)
    nuevo_tweet = ' '.join(nuevo_tweet)
    return nuevo_tweet


stop_words = set(stopwords.words())
ps = nltk.stem.PorterStemmer()

with open('tweetsStemming.csv', 'w', newline = '') as archivo:
    csv_writer = csv.writer(archivo)
    with open('tweetsLimpios.csv', 'r') as f:
        contenido = f.readlines()
        n_linea = 0
        for tweet in contenido:
            tweet = tweet.strip()
            tweet = tweet.split(',')
            if 'rt' in tweet[2]: continue
            tweet[2] = quitarStop(tweet[2])
            tweet[2] = stemming(tweet[2])
            if len(tweet[2]) == 0: continue
            csv_writer.writerow(tweet)
            
print("Tiempo:", datetime.now() - inicio)
