#!/Users/az49/anaconda/bin/python

import sys
import nltk
import csv
import ast
from operator import itemgetter
import random

#unigrams = nltk.defaultdict(list) #key is word, value is category
unigrams = nltk.defaultdict(str) #key is word, value is category
bigrams = nltk.defaultdict(str) #key is bigram, value is category
trigrams = nltk.defaultdict(str) #key is trigram, value is category

unigram_cat_weighting = {'circulatory':15.2133333333333,
'digestive':10.5648148148148,
'endocrine':5.00438596491228,
'infections':2.8525,
'injury':49.6086956521739,
'mental':10.0973451327434,
'neoplasms':16.7794117647059,
'pregnancy':19.0166666666667,
'respiratory':17.2878787878788}

bigram_cat_weighting = {'circulatory':9.65931863727455,
'digestive':11.1832946635731,
'endocrine':8.60714285714286,
'infections':5.09513742071882,
'injury':4.75814412635735,
'mental':10.8558558558559,
'neoplasms':21.8099547511312,
'pregnancy':11.6707021791768,
'respiratory':16.4505119453925}

trigram_cat_weighting = {'circulatory':9.04258943781942,
'digestive':13.1386138613861,
'endocrine':11.6916299559471,
'infections':9.56396396396396,
'injury':2.74173553719008,
'mental':15.7507418397626,
'neoplasms':19.5147058823529,
'pregnancy':10.7886178861789,
'respiratory':19.5867158671587}

#with open('unigram_cat.csv', 'rb') as csvfile:
#	unireader = csv.reader(csvfile, delimiter='|', quotechar='"')
with open('unigram_cat_final.csv', 'rb') as csvfile:
	unireader = csv.reader(csvfile, delimiter='\t')
	for row in unireader:
		#print row
		#unigrams[row[0]] = list(ast.literal_eval(row[1]))
		unigrams[row[0]] = row[1]

#print unigrams

#with open('bigram_cat.csv', 'rb') as csvfile:
	#bireader = csv.reader(csvfile, delimiter='|', quotechar='"')
with open('bigram_cat_final.csv', 'rb') as csvfile:
	bireader = csv.reader(csvfile, delimiter='\t')
	for row in bireader:
		#bigrams[row[0]] = list(ast.literal_eval(row[1]))
		bigrams[tuple(ast.literal_eval(row[0]))] = row[1]

#with open('trigram_cat.csv', 'rb') as csvfile:
	#trireader = csv.reader(csvfile, delimiter='|', quotechar='"')
with open('trigram_cat_final.csv', 'rb') as csvfile:
	trireader = csv.reader(csvfile, delimiter='\t')
	for row in trireader:
		#trigrams[row[0]] = list(ast.literal_eval(row[1]))
		trigrams[tuple(ast.literal_eval(row[0]))] = row[1]

#print type(trigrams.keys()[0])

#print "number of final unigrams: " + str(len(unigrams.keys()))
#print "number of final bigrams: " + str(len(bigrams.keys()))
#print "number of final trigrams: " + str(len(trigrams.keys()))

#load titles
#split into words, bigrams, trigrams
#test word in unigrams dict, return category (single), add category to pmid/category/weighting dict
#test pair in bigrams dict, return category (single), add category to pmid/category/weighting dict (weight more than word)
#test triad in trigrams dict, return category (single), add category to pmid/category/weighting dict (weight most)
#go through pmid/category/weighting dict and select category with highest weighting for each pmid

pubcat = {}

#with open('some_titles.txt', 'rb') as csvfile:
with open(sys.argv[1], 'rb') as csvfile:
	with open('pmid_disease' + str(random.randint(1,99999)) + '.csv', 'wb') as pubfile:
		with open('cat_matches.csv', 'wb') as qafile:
			titlesreader = csv.reader(csvfile, delimiter='|', escapechar='\\')
			recordwriter = csv.writer(pubfile, delimiter='|', quotechar='"', escapechar='\\')
			qawriter = csv.writer(qafile, delimiter="|", quotechar='"')
			for row in titlesreader:
				#print row
				cfdist = nltk.ConditionalFreqDist()
				cats_weighted = nltk.defaultdict(int)
				title_words = [w.lower() for w in nltk.RegexpTokenizer(r'\w+').tokenize(row[2])]
				#print title_words
				for w in set(title_words):
					#if w in unigrams.keys():
					if w in unigrams:
						#print w, "matching word to cat", unigrams[w]
						#cfdist["unigram"].inc(unigrams[w][0])
						cfdist["unigram"].inc(unigrams[w])
						qawriter.writerow([row[0],w,unigrams[w]])
				for bigram in set(nltk.bigrams(title_words)):
					#print "looking for", bigram, "of type", type(bigram)
					#if bigram in bigrams.keys():
					if bigram in bigrams:
						#print bigram, "matching bigram to cat", bigrams[bigram]
						#cfdist["bigram"].inc(bigrams[bigram][0])
						cfdist["bigram"].inc(bigrams[bigram])
						qawriter.writerow([row[0],bigram,bigrams[bigram]])
				for trigram in set(nltk.trigrams(title_words)):
					#print "looking for", trigram, "of type", type(trigram)
					#if trigram in trigrams.keys():
					if trigram in trigrams:
						#print trigram, "matching trigram to cat", trigrams[trigram]
						#cfdist["trigram"].inc(trigrams[trigram][0])
						cfdist["trigram"].inc(trigrams[trigram])
						qawriter.writerow([row[0],trigram,trigrams[trigram]])
				for cat in cfdist["unigram"]:
					cats_weighted[cat] += .1 * cfdist["unigram"][cat] * unigram_cat_weighting[cat]
					#print cat, cats_weighted[cat]
				for cat in cfdist["bigram"]:
					cats_weighted[cat] += .5 * cfdist["bigram"][cat] * bigram_cat_weighting[cat]
					#print cat, cats_weighted[cat]
				for cat in cfdist["trigram"]:
					cats_weighted[cat] += 1 * cfdist["trigram"][cat] * trigram_cat_weighting[cat]
					#print cat, cats_weighted[cat]
				cats_sorted = sorted(cats_weighted.items(), key=itemgetter(1), reverse=True)
				#print cats_sorted
				if len(cats_sorted) == 1:
					pubcat[row[0]] = cats_sorted[0][0]
				elif len(cats_sorted) > 1:
					if cats_sorted[0][1] > cats_sorted[1][1]:
						pubcat[row[0]] = cats_sorted[0][0]
				#if row[0] in pubcat.keys():
				if row[0] in pubcat:
					#print row[0], pubcat[row[0]]
					recordwriter.writerow([row[0],pubcat[row[0]],row[1],row[2],row[3]])
