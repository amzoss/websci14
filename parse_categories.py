#!/Users/az49/anaconda/bin/python

import nltk
import csv
#from operator import itemgetter

unigrams = nltk.defaultdict(list) #key is word, value is category
bigrams = nltk.defaultdict(list) #key is bigram, value is category
trigrams = nltk.defaultdict(list) #key is trigram, value is category

#with open('some_categories.txt', 'rb') as csvfile:
with open('ICD10_tabular_categorized_stripped.out', 'rb') as csvfile:
	catreader = csv.reader(csvfile, delimiter='\t', quotechar='"')
	for row in catreader:
		words = [w.lower() for w in nltk.RegexpTokenizer(r'\w+').tokenize(row[0])]
		subcat_words = [w.lower() for w in nltk.RegexpTokenizer(r'\w+').tokenize(row[1])]
		for w in set(words + subcat_words):
			if row[0] not in unigrams[w]:
				unigrams[w].append(row[0])
		for bigram in set(nltk.bigrams(words) + nltk.bigrams(subcat_words)):
			if row[0] not in bigrams[bigram]:
				bigrams[bigram].append(row[0])
		for trigram in set(nltk.trigrams(words) + nltk.trigrams(subcat_words)):
			if row[0] not in trigrams[trigram]:
				trigrams[trigram].append(row[0])

print "number of unigrams: " + str(len(unigrams.keys()))
print "number of bigrams: " + str(len(bigrams.keys()))
print "number of trigrams: " + str(len(trigrams.keys()))

del_from_unigrams = []
del_from_bigrams = []
del_from_trigrams = []

for word in unigrams:
	if len(unigrams[word]) > 1 or word.isdigit() or word in nltk.corpus.stopwords.words('english'):
		del_from_unigrams.append(word)

for pair in bigrams:
	if len(bigrams[pair]) > 1 or (pair[0] in nltk.corpus.stopwords.words('english') and pair[1] in nltk.corpus.stopwords.words('english')):
		del_from_bigrams.append(pair)

for triad in trigrams:
	if len(trigrams[triad]) > 1 or (triad[0] in nltk.corpus.stopwords.words('english') and triad[1] in nltk.corpus.stopwords.words('english') and triad[2] in nltk.corpus.stopwords.words('english')):
		del_from_trigrams.append(triad)

for word in del_from_unigrams:
	del unigrams[word]

for pair in del_from_bigrams:
	del bigrams[pair]

for triad in del_from_trigrams:
	del trigrams[triad]

print "number of final unigrams: " + str(len(unigrams.keys()))
print "number of final bigrams: " + str(len(bigrams.keys()))
print "number of final trigrams: " + str(len(trigrams.keys()))

with open('unigram_cat.csv', 'wb') as unifile:
	recordwriter = csv.writer(unifile, delimiter="|", quotechar='"')
	for pair in unigrams.items():
		recordwriter.writerow(pair)

with open('bigram_cat.csv', 'wb') as bifile:
	recordwriter = csv.writer(bifile, delimiter="|", quotechar='"')
	for pair in bigrams.items():
		recordwriter.writerow(pair)

with open('trigram_cat.csv', 'wb') as trifile:
	recordwriter = csv.writer(trifile, delimiter="|", quotechar='"')
	for pair in trigrams.items():
		recordwriter.writerow(pair)
