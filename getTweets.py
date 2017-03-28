#!/usr/bin/env python
# -*- coding: utf-8 -*-
import GetOldTweets.got3 as got
import tweepy
from langdetect import detect
import csv
import sys

# Create variables for each key, secret, token
consumer_key = 'kJCKcjHi0ffCL8qckgywLct5P'
consumer_secret = 're6vu4Y9ttmmkZ4ks80prrAZWNgzPAOQntMLiTPKdiO2ms5WMG'
access_token = '846018269400256514-09MOwPk5ftW9wSgKu5aHB3HT3kz66bt'
access_token_secret = 'Rgabs0Jmbin6SCVEA6ixnnfAlmUrtL1go8JbD630xwAXs'
# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

scentences_friend = []

def writeTweetInFile(friend,writer,busqueda,tukky):
	tweet = []
	try:
		tweetCriteria = got.manager.TweetCriteria().setUsername(friend.screen_name
							).setQuerySearch(busqueda).setSince("2016-10-01"
							).setUntil("2017-01-01").setMaxTweets(20)
		tweet = got.manager.TweetManager.getTweets(tweetCriteria)
	except:
		print("fallo")

	if tweet:
		# Print tweets
		for t in tweet:
			if not t.text in scentences_friend and "es" == detect(t.text):
				scentences_friend.append(t.text)
				writer.writerow([friend.screen_name,t.text,t.retweets,tukky])
				print(t.text)
				print("----------------------------------")

		return len(tweet)

	return 0

def main(argv):
	type_tweets = int(argv[2])
	csv_file = open("Datos/"+argv[1], "w", newline='')
	writer = csv.writer(csv_file, delimiter=',')
	writer.writerow(["USERNAME","TEXT","RETWEETS","ABOUT_BASEBALL"])

	baseball_kw = [ 'magallanes','leones del caracas','cardenales de lara','beisbol',
					'tigres de aragua','tiburones de la guaira','caribes de anzoategui',
					'aguilas del zulia','lvbp','bravos de margarita','baseball']
	normal_kw = [ 	'cine','restaurante','pasear','perros de la calle','simon bolivar',
					'socialismo','grammy','pelicula','comida','computacion','linux',
					'opsu','poemas','musica','aeropuerto','empanada','fundacion']

	friends = tweepy.Cursor(api.friends).items()
	for friend in friends:	
		len_tweets = 0
		if type_tweets == 1:
			for kw in baseball_kw:
				len_tweets += writeTweetInFile(friend,writer,kw,1)
				if len_tweets > 12:
					break
		else:
			for kw in normal_kw:
				len_tweets += writeTweetInFile(friend,writer,kw,0)
				if len_tweets > 12:
					break
		del scentences_friend[:]
	
	csv_file.close()
	
if __name__ == '__main__':
	main(sys.argv)
