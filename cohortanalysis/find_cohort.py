# -*- coding: utf-8 -*-
import os
import csv
import argparse 

__author__ = "S. May"

"""Determines which students were sent which surveys, and which students were sent all four surveys. 
Saves results within a results sub-directory.
Students are identified by their emails, which are unique even after graduating.
Both student emails and student_ids are stored in the output file. 
"""

def find_cohort(file_names, keycol, idcol):
	"""Given a list of file names, writes to a results file the names of each 
	student_id, corresponding email, and the surveys they were sent.  The ids and emails 
	who were sent all four surveys are also written to a cohort.csv file. 
	""" 
	cd = os.getcwd()
	survey_dict = {}

	for file in file_names: 
		print "\nLOOKING AT FILE:", file
		survey_dict = get_surveylist(file, keycol, idcol, survey_dict)

	# set up results directory and files. WILL DELETE any pre-existing
	# csv files named results.csv / cohort.csv within a results subdirectory
	if not os.path.isdir(cd + "/results"): 
		os.mkdir("results")
	if os.path.isfile(cd + "/results/cohort.csv"): 
		os.remove(cd + "/results/cohort.csv")
	if os.path.isfile(cd + "/results/results.csv"): 
		os.remove(cd + "/results/results.csv")

	os.chdir(cd +"/results")

	cohort_csv = open(cd+"/results/cohort.csv", "w+")
	w_cohort = csv.writer(cohort_csv)
	results_csv = open(cd+"/results/results.csv", "w+")
	w_results = csv.writer(results_csv)

	for key, values in survey_dict.iteritems():  
		row = [key] + values
		w_results.writerow(row)
		if len(values) == len(file_names): 
			w_cohort.writerow(row)

def get_surveylist(file, keycol, idcol, survey_dict): 
	"""Given a .csv file, the name of email/id columns, and a survey_dict that maps students
	by email and id to surveys, updates the survey_dict for the current file.
	"""
	cd = os.getcwd()
	#print "\ncurrent working directory:",cd, "\n"
	with open(cd + "/" + file, "rU") as f: 
		rd_f = csv.reader(f)
		f_list = list(rd_f)

	for row in f_list:
		if row[keycol] in survey_dict:
			survey_dict[row[keycol]].append(file.split('.')[0] + ":::" + row[idcol])
		else: 
			survey_dict[row[keycol]] = [file.split('.')[0]+ ":::" + row[idcol]]

	return survey_dict

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("directory", 
		help="name of sub-directory containing csv data files", 
		type=str)
	parser.add_argument("keycol", 
		help="index of col containing key that is consistant across files", 
		type=int)
	parser.add_argument("idcol", 
		help="index of col containing the unique id for the data file", 
		type=int)
	args = parser.parse_args()
	cd = os.getcwd() 

	file_names = []
	for file in os.listdir(cd + "/" + args.directory): 
		form = file.split('.')
		if len(form) > 1: 
			form = form[1]
			if form == 'csv': 
				file_names.append(args.directory + "/" + file)
	find_cohort(file_names, args.keycol, args.idcol)
	print "\nDONE.\n"
