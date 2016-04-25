import argparse
import os
import csv
from nltk import pos_tag
from nltk.tokenize import word_tokenize

__author__ = "S. May"

"""Given a csv file, where each row is a comment, writes a table to a new csv file 
where each row is a comment, each column is a noun, and the cells are a boolean (1, 0)
indicating 1: the noun appears in the comment, or 0: the noun does not appear in the 
comment.  Only nouns that appear in > threshold number of comments are included.
"""

def get_nouns(f_list):
	"""Returns a dictionary of all nouns in the comments mapped to their frequencies.
	A noun will only be counted once per comment.
	"""
	top_nouns = {}
	for line in f_list: 
		tagged = tag_speech(line[0])
		this_comment = []
		for word, tag in tagged: 
			if tag == 'NOUN':
				if word not in top_nouns.keys():
					top_nouns.update({word: 0})
				if word not in this_comment:
					top_nouns[word] += 1
					this_comment.append(word)

	return top_nouns

def tag_speech(sent):
	"""Universal part of speech tagging for a sentence. 
	"""
	return pos_tag(word_tokenize(sent), tagset='universal')

def tag_file(file_list, top_nouns, threshold):
	"""For every comment in file_list, writes a row to a csv file containing (1) the comment, 
	and (2) a series of 1's and 0's representing whether or not a noun appears in the comment. 
	The nouns for each column appear as headers in the first row.  Only nouns with frequency > 
	threshold are recorded. 
	"""
	cd = os.getcwd()

	if os.path.isfile(cd + "/results.csv"): 
		os.remove("results.csv")

	results = open("results.csv", 'w+')
	results_writer = csv.writer(results)

	headers = [""]
	for noun, freq in top_nouns.items():
		if freq > threshold: 
			headers.append(noun)

	results_writer.writerow(headers)

	for comment in file_list: 
		new_row = comment
		for noun, freq in top_nouns.items(): 
			if freq > 3:
				if noun in comment[0]: 
					new_row.append("1")
				else: 
					new_row.append("0")
		results_writer.writerow(new_row)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('filename', type=str, help="name of csv file holding comments")
	parser.add_argument('threshold', type=int, help="threshold for inclusion of word")
	args = parser.parse_args()

	with open(args.filename) as f: 
		f_reader = csv.reader(f)
		f_list = list(f_reader)

	top_nouns = get_top_nouns(f_list)
	print "Extracted noun counts"
	tag_file(f_list, top_nouns, args.threshold)
	print "DONE. Written to file."

	

	