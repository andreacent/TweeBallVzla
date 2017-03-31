#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re,string
from nltk.corpus import stopwords
import unicodedata
import Stemmer
import numpy as np
import csv

words_stemmer = {}
words_dict = {}

##############################################
# Transform data to suitable format
# @param {String} d 
# @param [String] words 
def getListData(d,words):
	new_data = []
	for i in range(len(words)):
		word_in_d = words[i] in d
		new_data.append(1 if word_in_d else 0)
		if word_in_d:
			d.remove(words[i])
	return new_data

##############################################
# Transform data to suitable format
# @param [[[String],Int]] data 
# @param [String] words 
def transformData(data,words):
	d_input,d_target = [],[]
	for d in data:
		d_input.append(getListData(d[0],words))
		d_target.append(d[1])
	return d_input,d_target 

##############################################
# Write file with stemming's words
# @param String filename 
# @param {String:{String}} words_stemmer
def writeStemmingFile(filename,words_stemmer):
	data_file = open(filename,'w')
	data_file.write("### <Raiz> -> <Palabras> ###")
	for k,v in words_stemmer.items():
		data_file.write("\n"+k +" -> ")
		for w in v:
			data_file.write(w+" ")
	data_file.close()

##############################################
# Cota minima de cantidad de ocurrencias de una 
# palabra para ser tomada en cuenta
def getCota():
	#max_fcy = max(words_dict.values())
	sum_ocu = 0
	for k,v in words_dict.items():
		sum_ocu += v
	average = sum_ocu / len(words_dict)
	cota = round(average*0.4)
	print(cota)
	return cota if cota > 1 else 1

##############################################
# Read file
# @param String filename : file with data
def readTrainingData(filename):
	data = []

	with open(filename, 'r', encoding="utf-8") as data_file:
		reader = csv.reader(data_file)
		next(reader)
		for l in reader:
			try:
				tukky = int(l[3]) 
				important_words = textFilter(l[1].lower())

				if important_words:
					data.append( [ important_words, tukky ] )
					#print(l[1])
					#print(important_words)
					#print("--------------------------------")
			except:
				pass

		np.random.shuffle(data)

	cota = getCota()
	words = []
	for k,v in words_dict.items():
		if v > cota:
			words.append(k)
		else:
			words_stemmer.pop(k,None)

	writeStemmingFile("Datos/stemming.txt",words_stemmer)

	words_stemmer.clear()
	words_dict.clear()

	return data,words

##############################################
# Say if string is a number
# @param String inputString
def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

##############################################
# Say if string is a link
# @param String x
def isLink(x):
	return x.find("http") >= 0 or x.find(".com") >= 0 or x.find("/") >= 0

##############################################
# Say if string is not a valid hashtag
# @param String x
def isHashtag(x):
	sig_words = ['magallanes','leones','cardenales','tigres',
					'tiburones','bravos','aguilas',
					'caribes','lvbp','baseball','beisbol']
	#si el hashtag contiene las palabras anteriores entonces es valido
	if x[0]=="#":
		return False if x[1:].lower() in sig_words else True
	return False

##############################################
# Detect words in text
# Delete stopwords and do stemming
# @param String text
def textFilter(text):	
	#elimina tildes
	scentence = ''.join((c for c in unicodedata.normalize('NFD',text) if unicodedata.category(c) != 'Mn')) 
	words = [x for x in scentence.split() if not (hasNumbers(x) or x[0]=="@" or isHashtag(x) or isLink(x))]
	#remove punctuation and split into seperate words
	words = re.findall(r'\w+', " ".join(words),flags = re.UNICODE | re.LOCALE)

	stemmer = Stemmer.Stemmer('spanish') 	#stemming
	stop_words = stopwords.words('spanish') #stopwords

	important_words = set()
	for w in words:
		if w in ["sr","sra"]:
			pass
		elif w not in stop_words:		#stopwords
			word = stemmer.stemWord(w)	#stemming
			important_words.add(word)

			words_dict[word] = words_dict[word]+1 if word in words_dict else 1

			if not word in words_stemmer:
				words_stemmer[word] = set()
			words_stemmer[word].add(w)

	return important_words