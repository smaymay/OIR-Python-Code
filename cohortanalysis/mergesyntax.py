import os
import csv
import argparse 

__author__ = "S. May"

"""Given a csv file containing a mapping of student email to id within each file,
writes the SPSS syntax to add a uniform id across all data files to the 
SPSS file, to facilitate merging files. 
"""
def get_mergesyntax(csvmap, variable_names, variable_types): 
	""" Given a file mapping email to id for each file, produces the spss syntax to
	add a uniform id to each data file, and a boolean 1 to indicate yes if part of 
	cohort.

	for 2015 cohort: variable_names = [studyid, V1, studyID, V1]; 
	variable_types = [i, s, i, s]
	"""
	cd = os.getcwd()

	with open(cd + "/" + csvmap) as c: 
		rd_csv = csv.reader(c)
		map_list = list(rd_csv)
	headers = map_list[0]
	del map_list[0]

	num_strings = len(headers)-1
	strings = [[] for i in xrange(0, num_strings)]
	cohort_strings = [[] for i in xrange(0, num_strings)]

	merge_file = open("mergesyntax.txt", "w") 
	num_rows = len(map_list)

	for i in xrange(0, num_rows): 
		row = map_list[i]
		s = row[0]
		# set boolean default = True that student is cohort
		cohort = True
		for j in xrange(1, num_strings+1):
			if row[j] != '': 
				if variable_types[j-1] == "s":
					strings[j-1].append(
						"if " + variable_names[j-1] + " = \"" + row[j] + "\" cohortid = " + str(i) + ".\n")
				else: 
					strings[j-1].append(
						"if " + variable_names[j-1] + " = " + row[j] +  " cohortid = " + str(i) + ".\n")
			else: 
				cohort = False
		if cohort: 
			for j in xrange(0, num_strings): 
				if variable_types[j] == "s": 
					cohort_strings[j].append(
						"if " + variable_names[j] + " = \"" + row[j+1] + "\" iscohort = 1.\n")
				else:
					cohort_strings[j].append(
						"if " + variable_names[j] + " = " + row[j+1] + " iscohort = 1.\n")

	for i in xrange(0, num_strings): 
		merge_file.write("\n\n" + headers[i+1] + "\n\n")
		for j in xrange(0, len(strings[i])): 
			merge_file.write(strings[i][j])
		merge_file.write("\n\n")
		for j in xrange(0, len(cohort_strings[i])): 
			merge_file.write(cohort_strings[i][j])
		merge_file.write("\n\n*****************\n\n")
	print "\nDONE.\n"
