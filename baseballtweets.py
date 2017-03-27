#!/usr/bin/env python
# -*- coding: utf-8 -*-
import GetOldTweets.got3 as got
import tweepy
import re,string
from nltk.corpus import stopwords
import unicodedata
import Stemmer
from langdetect import detect

# Create variables for each key, secret, token
consumer_key = 'kJCKcjHi0ffCL8qckgywLct5P'
consumer_secret = 're6vu4Y9ttmmkZ4ks80prrAZWNgzPAOQntMLiTPKdiO2ms5WMG'
access_token = '846018269400256514-09MOwPk5ftW9wSgKu5aHB3HT3kz66bt'
access_token_secret = 'Rgabs0Jmbin6SCVEA6ixnnfAlmUrtL1go8JbD630xwAXs'
# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

words_stemmer = {}
scentences_friend = []

def textFilter(text):	
	#elimina tildes
	scentence = ''.join((c for c in unicodedata.normalize('NFD',text) if unicodedata.category(c) != 'Mn')) 
	words = [x for x in scentence.split() if x[0]!="@" and x[0]!="#"]
	#remove punctuation and split into seperate words
	words = re.findall(r'\w+', " ".join(words),flags = re.UNICODE | re.LOCALE)

	stemmer = Stemmer.Stemmer('spanish') 	#stemming
	stop_words = stopwords.words('spanish') 	#stopwords

	important_words =[]
	for w in words:
		if w in ["sr"]:
			pass
		elif w not in stop_words:			#stopwords
			word = stemmer.stemWord(w)	#stemming
			if not word in important_words:
				important_words.append(word)

			if word in words_stemmer:
				words_stemmer[word].append(w)
			else:
				words_stemmer[word] = [w]

	return important_words

def writeTweetInFile(friend,data_file,busqueda):
	tweetCriteria = got.manager.TweetCriteria().setUsername(friend.screen_name
						).setQuerySearch(busqueda).setSince("2016-08-01"
						).setUntil("2017-02-01").setMaxTweets(12)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)
	# Print tweets
	for t in tweet:
		if not t.text in scentences_friend and "es" == detect(t.text):
			scentences_friend.append(t.text)
			data_file.write(friend.screen_name +","+t.text+","+str(t.retweets)+"\n")
			#important_words = textFilter(t.text.lower())
			print(t.text)
			#print(important_words)
			print("----------------------------------")

def main():
	data_file = open("datos.csv",'w')
	data_file.write("USERNAME,TEXT,RETWEETS\n")

	friends = tweepy.Cursor(api.friends).items()
	for friend in friends:
		writeTweetInFile(friend,data_file,'magallanes')
		writeTweetInFile(friend,data_file,'leones del caracas')
		writeTweetInFile(friend,data_file,'cardenales de lara')
		writeTweetInFile(friend,data_file,'tigres de aragua')
		writeTweetInFile(friend,data_file,'tiburones de la guaira')
		writeTweetInFile(friend,data_file,'bravos de margarita')
		writeTweetInFile(friend,data_file,'aguilas del zulia')
		writeTweetInFile(friend,data_file,'caribes de anzoategui')
		writeTweetInFile(friend,data_file,'lvbp')
		writeTweetInFile(friend,data_file,'baseball')
		writeTweetInFile(friend,data_file,'beisbol venezuela')
		writeTweetInFile(friend,data_file,'sabios del vargas')
		del scentences_friend[:]
	
	data_file.close()
	
if __name__ == '__main__':
	main()
