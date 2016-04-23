import os
import xlrd, csv

__author__ = "S. May"

""" Helper methods for developing cohort from multiple surveys"""

def csv_from_excelsheets(file, sheets): 
	"""
	Given the name of an .xls or .xlsx file and a list of sheets within the excel file, converts
	the sheet(s) to .csv files and saves in subfolder csv. 
	Returns the name(s) of the csv files in a list. 
	"""
	wb = xlrd.open_workbook(file)
	cd = os.getcwd()
	sheetnames = []

	for i in xrange(0, len(sheets)): 
		s = wb.sheet_by_name(sheets[i])
		file_name = file.split('.')[0]

		if not os.path.isdir(cd + "/csv"): 
			os.mkdir("csv")

		s_formated_name = sheets[i].split(' ')[0]
		s_name = file_name + "_" + s_formated_name + ".csv"
		if os.path.isfile(cd + "/csv/" + s_name): # remove any pre-existing file of same name
			os.remove(cd + "/csv/" + s_name)

		s_csv = open(cd + "/csv/" + s_name, 'w+')
		s_writer = csv.writer(s_csv)

		for row_num in xrange(s.nrows): 
			s_writer.writerow(s.row_values(row_num))
		s_csv.close()

		sheetnames.append(s_name)

	return sheetnames

def replace_ids(newidfile, oldidfile, column_list, map_keys): 
	"""Mailing lists sometimes matched student emails to incorrect ids -- e.g. ids that mapped to multiple students,
	or ids which did not correspond to the ids used to identify students within a data file.  Given the name of a .csv
	file containing a column of emails and a column of correct ids, and the name of the file withthe incorrect mapping, 
	writes a file containing the correct mapping. 
	To do this, takes in a list of columns in the newidfile to transfer over, and 
	a list of mapkeys, with the first entry being the map key for the newidfile
	and the second entry being the mapkey for the oldidfile. 
	"""
	cd = os.getcwd()
	with open(oldidfile) as oldf:
		rd_old = csv.reader(oldf)
		old_list = list(rd_old)

	with open(newidfile) as newf: 
		rd_new = csv.reader(newf)
		new_list = list(rd_new)

	result_file_name = oldidfile.split('.')[0] + "_new.csv"
	if os.path.isfile(cd + "/" + result_file_name):
		os.remove(cd + "/" + result_file_name) # removes any pre-existing iteration

	result_csv = open(cd + "/" + result_file_name, "w+")
	w_results = csv.writer(result_csv)

	old_headers = {old_list[0][i]: i for i in xrange(0, len(old_list[0]))}
	del old_list[0]
	new_headers = {new_list[0][i]: i for i in xrange(0, len(new_list[0]))}
	del new_list[0]

	new_mapkey = map_keys[0]
	old_mapkey = map_keys[1]
	# create dictionary mapping emails to rows in newidfile
	student_dict = {new_list[row][new_headers[new_mapkey]]: row for row in xrange(0, len(new_list))}

	for row1 in old_list:
		student = row1[old_headers[old_mapkey]] # gets student email

		# sometimes all the students in the mailing list might not be in the newid file --
		# e.g. if the new id file has only those students who responded to the survey
		if student in student_dict: 
			row2 = student_dict[student] # gets row of student in newidfile
			new_row = [student]

			for col in column_list: # adds values of [row][col] for each col selected col in newidlist
				new_row.append(new_list[row2][new_headers[col]])

			w_results.writerow(new_row)

	return result_file_name

def organize_results(filemap, results):
	"""Given a results.csv file created by find_cohort, and a filemap mapping the files
	from which results was created to data files to be merged, writes a .csv file in the results
	subfold with col[0] = email, col[1] = 1st data file id, col[2] = 2nd data file id, etc. Saves
	as results_organized.csv.
	""" 
	cd = os.getcwd()

	with open(results) as r: 
		rd = csv.reader(r)
		results_list = list(rd)

	headers = filemap.values()
	keys = filemap.keys()
	# delete result of any pre-existing iteration
	if os.path.isfile(cd + "/results_organized.csv"): 
		os.remove(cd + "/results_organized.csv") # 

	result_csv = open(cd + "/results_organized.csv", "w+")
	w_results = csv.writer(result_csv)
	# write header row
	w_results.writerow(['email'] + headers)

	for row in results_list: 
		new_row = [row[0]] + ['' for i in xrange(0, len(filemap.values()))]
		for i in xrange(1, len(row)):
			f = row[i].split(':::')[0]
			student_id = row[i].split(':::')[1]
			new_row[headers.index(filemap[f])+1] = student_id
		print "\n"
		w_results.writerow(new_row)
	print "\nDONE.\n"

