import argparse
import os
import csv
from nltk import pos_tag
from nltk.tokenize import word_tokenize

__author__ = "S. May"

"""Given a csv file, where each row is a comment, writes a table to a new csv file 
where each row is a comment, each column is a word of type POS, specified as an input argument, 
and the cells are a boolean (1, 0) indicating 1: the word appears in the comment, or 0: the word 
does not appear in the comment.  Only nouns that appear in > threshold number of comments are included.
"""

def get_words(f_list, pos):
	"""Returns a dictionary of all nouns in the comments mapped to their frequencies.
	A noun will only be counted once per comment.
	"""
	top_words = {}
	for line in f_list: 
		tagged = tag_speech(line[0])
		this_comment = []
		for word, tag in tagged: 
			if tag == pos:
				if word not in top_words.keys():
					top_words.update({word: 0})
				if word not in this_comment:
					top_words[word] += 1
					this_comment.append(word)

	return top_words

def tag_speech(sent):
	"""Universal part of speech tagging for a sentence. 
	"""
	return pos_tag(word_tokenize(sent), tagset='universal')

def tag_file(file_list, top_words, threshold, pos):
	"""For every comment in file_list, writes a row to a csv file containing (1) the comment, 
	and (2) a series of 1's and 0's representing whether or not a noun appears in the comment. 
	The nouns for each column appear as headers in the first row.  Only nouns with frequency > 
	threshold are recorded. 
	"""
	cd = os.getcwd()

	filename = "results-" + pos + "-" + str(threshold) + ".csv"

	if os.path.isfile(cd + "/" + filename): 
		os.remove(filename)

	results = open(filename, 'w+')
	results_writer = csv.writer(results)

	headers = [""]
	for word, freq in top_words.items():
		if freq >= threshold: 
			headers.append(word)

	results_writer.writerow(headers)

	for comment in file_list: 
		new_row = comment
		for word, freq in top_words.items(): 
			if freq > 3:
				if word in comment[0]: 
					new_row.append("1")
				else: 
					new_row.append("0")
		results_writer.writerow(new_row)

	return filename


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('filename', type=str, help="name of csv file holding comments")

	# just added all of the universal POS tags I could think of ... feel free to add
	# to this list as needed 
	parser.add_argument('pos', type=str, 
		choices=['DET', 'VERB', 'ADV', 'ADJ', 'NOUN', 'ADP'],
		help="pos to select from words")

	parser.add_argument('threshold', type=int, help="threshold for inclusion of word")
	args = parser.parse_args()

	with open(args.filename) as f: 
		f_reader = csv.reader(f)
		f_list = list(f_reader)

	top_words = get_words(f_list, args.pos)
	print "Extracted " + args.pos + " counts"
	output_file = tag_file(f_list, top_words, args.threshold, args.pos)
	print "DONE. Written to file: ", output_file