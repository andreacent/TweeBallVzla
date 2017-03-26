#!/usr/bin/env python
# -*- coding: utf-8 -*-
import GetOldTweets.got3 as got
import tweepy
import re,string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import unicodedata

# Create variables for each key, secret, token
consumer_key = 'kJCKcjHi0ffCL8qckgywLct5P'
consumer_secret = 're6vu4Y9ttmmkZ4ks80prrAZWNgzPAOQntMLiTPKdiO2ms5WMG'
access_token = '846018269400256514-09MOwPk5ftW9wSgKu5aHB3HT3kz66bt'
access_token_secret = 'Rgabs0Jmbin6SCVEA6ixnnfAlmUrtL1go8JbD630xwAXs'

def printTweet(descr, t):
	print (descr)
	print ("Username: %s" % t.username)
	print ("Retweets: %d" % t.retweets)
	print ("Text: %s" % t.text)
	print ("Mentions: %s" % t.mentions)
	print ("Hashtags: %s\n" % t.hashtags)

def elimina_tildes(cadena):
	# http://guimi.net
	# Cambiamos caracteres modificados (áüç...) por los caracteres base (auc...)
	# Basado en una función de Miguel en
	# http://www.leccionespracticas.com/uncategorized/eliminar-tildes-con-python-solucionado/
	s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
	return s

def detectarLenguaje(text_to_detect):
	languages = ["spanish","english"]
	tokens = word_tokenize(text_to_detect)
	tokens = [t.strip().lower() for t in tokens] # Convierte todos los textos a minúsculas para su posterior comparación

	lang_count = {}
	# Por cada idioma
	for lang in languages:
		# Obtenemos las stopwords del idioma del módulo nltk
		stop_words = stopwords.words(lang)
		lang_count[lang] = 0 # Inicializa a 0 el contador para cada idioma

		# Recorremos las palabras del texto a analizar
		for word in tokens:
			if word in stop_words: # Si la palabra se encuentra entre las stopwords, incrementa el contador
				lang_count[lang] += 1

	# Obtiene el idioma con el número mayor de coincidencias
	detected_language = max(lang_count, key=lang_count.get)

	return detected_language

def textFilter(t):
	#We only want to work with lowercase for the comparisons
	scentence = t.lower() 
	#elimina tildes
	scentence = elimina_tildes(scentence)
	words = [x for x in scentence.split() if x[0]!="@" and x[0]!="#"]
	#remove punctuation and split into seperate words
	words = re.findall(r'\w+', " ".join(words),flags = re.UNICODE | re.LOCALE)
	#This is the more pythonic way
	important_words = filter(lambda x: x not in stopwords.words('spanish'), words)

	return important_words

def main():

	# Set up OAuth and integrate with API
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth, wait_on_rate_limit=True)

	data_file = open("datos.csv",'w')
	data_file.write("USERNAME,TEXT,RETWEETS\n")

	friends = tweepy.Cursor(api.friends).items()
	for friend in friends:
		# Get tweets
		tweetCriteria = got.manager.TweetCriteria().setUsername(friend.screen_name
							).setQuerySearch('baseball').setSince("2016-08-01"
							).setUntil("2017-02-01").setMaxTweets(100)
		tweet = got.manager.TweetManager.getTweets(tweetCriteria)
		# Print tweets
		for t in tweet:
			if "spanish" == detectarLenguaje(t.text):
				data_file.write(friend.screen_name +","+t.text+","+str(t.retweets)+"\n")
			important_words = textFilter(t.text)
			print("----------------------------------")
			print(t.text)
			print(" ".join(important_words))
	
	data_file.close()
	
if __name__ == '__main__':
	main()
