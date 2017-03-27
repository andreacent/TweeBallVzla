#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re,string
from nltk.corpus import stopwords
import unicodedata
import Stemmer

words_stemmer = {}

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def textFilter(text):	
	#elimina tildes
	scentence = ''.join((c for c in unicodedata.normalize('NFD',text) if unicodedata.category(c) != 'Mn')) 
	words = [x for x in scentence.split() if not hasNumbers(x) and x[0]!="@" and x[0]!="#" and x.find("http") < 0 and x.find(".com") < 0 and x.find("/") < 0 ]
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