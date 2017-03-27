#!/usr/bin/env python
# -*- coding: utf-8 -*-
import GetOldTweets.got3 as got
import tweepy
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

scentences_friend = []

def writeTweetInFile(friend,data_file,busqueda,tukky):
	tweetCriteria = got.manager.TweetCriteria().setUsername(friend.screen_name
						).setQuerySearch(busqueda).setSince("2016-08-01"
						).setUntil("2017-02-01").setMaxTweets(20)
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)
	# Print tweets
	for t in tweet:
		if not t.text in scentences_friend and "es" == detect(t.text):
			scentences_friend.append(t.text)
			data_file.write(friend.screen_name +","+t.text+","+str(t.retweets)+","+str(tukky)+"\n")
			#print(t.text)
			#print("----------------------------------")

def main():
	data_file = open("datos.csv",'w')
	data_file.write("USERNAME,TEXT,RETWEETS,ABOUT_BASEBALL\n")

	friends = tweepy.Cursor(api.friends).items()
	for friend in friends:
		writeTweetInFile(friend,data_file,'magallanes',1)
		writeTweetInFile(friend,data_file,'leones del caracas',1)
		writeTweetInFile(friend,data_file,'cardenales de lara',1)
		writeTweetInFile(friend,data_file,'tigres de aragua',1)
		writeTweetInFile(friend,data_file,'tiburones de la guaira',1)
		writeTweetInFile(friend,data_file,'bravos de margarita',1)
		writeTweetInFile(friend,data_file,'aguilas del zulia',1)
		writeTweetInFile(friend,data_file,'caribes de anzoategui',1)
		writeTweetInFile(friend,data_file,'lvbp',1)
		writeTweetInFile(friend,data_file,'baseball',1)
		writeTweetInFile(friend,data_file,'beisbol venezuela',1)
		writeTweetInFile(friend,data_file,'sabios del vargas',1)
		del scentences_friend[:]
	
	data_file.close()
	
if __name__ == '__main__':
	main()
