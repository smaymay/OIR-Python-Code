from __future__ import division
import os, csv
import sys
import make_graphics as graphics
import numpy as np

__author__ = 'Sarah May'

"""Script to analyze TutorTrac data by producing .png figures and writing results
of preliminary research questions to a csv file.
"""

###################################################################
# open file, convert to list, and get headers
###################################################################
cd = os.getcwd()
with open(sys.argv[1]) as f: 
	rd_f = csv.reader(f)
	f_list = list(rd_f)

headers = f_list[0]
h_indices = {headers[i]: i for i in xrange(len(headers))}
del f_list[0]

###################################################################
# prep to loop through the file list and extract information
###################################################################
centers = ['APT', 'SI', 'Attached Tutoring', 'Assigned Tutoring']

# num visits will hold the number of visits by year by month for each center
num_visits = [[np.zeros(12) for y in xrange(4)] for c in xrange(4)]
# for students in SI only, get number of students going from each section in each year
num_visits_si = [{} for y in xrange(4)]
# unique_students holds the number of unique students going to each center by month and year
unique_students_month = [[[[] for m in xrange(12)] for y in xrange(4)] for c in xrange(0,4)]
unique_students_year = [[[] for y in xrange(4)] for c in xrange(4)]
#time_per_student gets the total amount of time spent by each student at each center by year
time_per_student = [[{} for y in xrange(4)] for c in xrange(4)]
# get the centers that students attend and the amount of time they spend there 
num_centers_student = [{} for y in xrange(4)]



###################################################################
# loop through file list to extract information
###################################################################
for row in f_list:

	# get center
	for center in centers: 
		if center in row[h_indices["SubcentersName"]]: 
			r_center = centers.index(center)

	year = row[h_indices["AY"]]
	month = row[h_indices["VisitsDateIn"]].split("/")[0]
	student = row[h_indices["STUID"]]
	section = row[h_indices["SectionsSubjectID"]]
	visit_time = float(row[h_indices["VisitsTotalTime"]])

	if year == "2011":
		yr_index = 0
	elif year == "2012":
		yr_index = 1
	elif year == "2013":
		yr_index = 2
	elif year == "2014":
		yr_index = 3

	# add one vist per row to appropriate center 
	num_visits[r_center][yr_index][int(month)-1] += 1

	# if center is SI, record by section 
	if centers[r_center] == 'SI':
		if section not in num_visits_si[yr_index]:
			num_visits_si[yr_index].update({section: 0})
		num_visits_si[yr_index][section] += 1

	# add student as having visited center if not already recorded
	if student not in unique_students_month[r_center][yr_index][int(month)-1]:
		unique_students_month[r_center][yr_index][int(month)-1].append(student)
	if student not in unique_students_year[r_center][yr_index]: 
		unique_students_year[r_center][yr_index].append(student)

	# add to total time for student at the center
	if student not in time_per_student[r_center][yr_index].keys(): 
		time_per_student[r_center][yr_index].update({student: visit_time})
	else:
		time_per_student[r_center][yr_index][student] += visit_time

	# record that student attended center -- and how long they stayed 
	if student not in num_centers_student[yr_index]: 
		num_centers_student[yr_index].update({student: {} for c in xrange(4)})
	if centers[r_center] not in num_centers_student[yr_index][student].keys():
		num_centers_student[yr_index][student].update({centers[r_center]: 0})
	num_centers_student[yr_index][student][centers[r_center]] += visit_time

###################################################################
# set up results.csv file
###################################################################
if os.path.isfile(cd + "/results.csv"):
	os.remove(cd + "/results.csv")

results_csv = open(cd + "/results.csv", "w+")
w_results = csv.writer(results_csv)

###################################################################
# make graphics and add to csv file
###################################################################

x_labels_months = np.array(range(1,13)*4, dtype=str)
x_labels_years = np.array(range(2011,2015), dtype=str)

###################################################################
# number of visits by month and by year by subcenter
by_month = [[] for i in xrange(4)]
by_year = [[] for i in xrange(4)]
i = 0
for center in num_visits: 
	by_year[i] = np.array([0]*4)
	j = 0
	for year in center:
		for m in year: 
			by_month[i].append(m)
		by_year[i][j] += np.sum(year)
		j += 1
	i += 1

# graphics
graphics.stacked_bar_chart(by_month, centers, x_labels_months,
	"Number of visits by month and subcenter",
	"visits_by_month")
graphics.stacked_bar_chart(by_year, centers, x_labels_years,
	"Number of visits by year and subcenter", 
	"visits_by_year")

for center in range(len(by_year)): 
	title = "Number of visits by year " + centers[center]
	figname = "num_visits_" + centers[center].split()[0]
	graphics.reg_bar_chart(by_year[center], x_labels_years, title, figname) 

# add to csv file
w_results.writerow(["Number of visits by month and subcenter"])
w_results.writerow(["MONTH"] + list(x_labels_months))
for center in xrange(len(by_month)):
	w_results.writerow([centers[center]] + by_month[center])
w_results.writerow([])
w_results.writerow(["Number of visits by year and subcenter"])
for center in xrange(len(by_year)):
	w_results.writerow([centers[center]] + list(by_year[center]))
w_results.writerow([])

###################################################################
# create pie showing number of visits by section by year for SI
# also add to csv file 

for year in xrange(4): 
	temp_labels = num_visits_si[year].keys()
	temp_vals = [v/np.sum(num_visits_si[year].values()) for v in num_visits_si[year].values()]
	# check to make sure vals add to 1
	# print np.sum(temp_vals)

	labels = []
	vals = []
	other = 0
	for i in range(len(temp_vals)):
		if temp_vals[i] > .01: 
			labels.append(temp_labels[i])
			vals.append(temp_vals[i]*100)
		else: 
			other += temp_vals[i]

	labels.append("other")
	vals.append(other*100)

	figname = "si_visits_by_section_"
	title = "SI visits by section, "
	if year == 0: 
		figname += "2011"
		title += "2011"
	elif year == 1: 
		figname += "2012"
		title += "2012"
	elif year == 2: 
		figname += "2013"
		title += "2013"
	elif year == 3:
		figname += "2014"
		title += "2014"

	graphics.pie_chart(vals, labels, title, figname)

	w_results.writerow([])
	w_results.writerow([title])
	w_results.writerow(temp_labels)
	w_results.writerow(num_visits_si[year].values())

w_results.writerow([])



###################################################################
# plot unique students by month and year
by_month = [[] for i in xrange(4)]
by_year = [[] for i in xrange(4)]

i = 0
for c in unique_students_month: 
	for y in c: 
		for m in y:
			by_month[i].append(len(m))
	i += 1
i = 0
for c in unique_students_year: 
	for y in c: 
		by_year[i].append(len(y))
	i += 1

graphics.stacked_bar_chart(by_month, centers, x_labels_months,
	"Number of unique students by month and subcenter",
	"unique_students_by_month")
graphics.stacked_bar_chart(by_year, centers, x_labels_years,
	"Number of unique students by year and subcenter", 
	"unique_students_by_year")

# add to csv file
w_results.writerow([])
w_results.writerow(["Number of unique students by month and subcenter"])
w_results.writerow(["MONTH"] + list(x_labels_months))
for center in xrange(len(by_month)):
	w_results.writerow([centers[center]] + by_month[center])
w_results.writerow([])
w_results.writerow(["Number of unique students by year and subcenter"])
for center in xrange(len(by_year)):
	w_results.writerow([centers[center]] + list(by_year[center]))
w_results.writerow([])

###################################################################
# plot average amounts of time students spend at each center by year
for center in xrange(len(time_per_student)):
	c = centers[center]
	title = "Average time per student at " + c + " by year"
	figname = "avg_time_per_student_" + c.split()[0]
	time_by_year = []
	for year in xrange(len(time_per_student[center])):
		time_by_year.append(np.average(time_per_student[center][year].values()))

	# make graphic
	graphics.reg_bar_chart(time_by_year, x_labels_years, title, figname)

	# add to csv file 
	w_results.writerow([])
	w_results.writerow([title + " (minutes), only for students who attended at least once"])
	w_results.writerow(x_labels_years)
	w_results.writerow(time_by_year)

###################################################################
# plot average number of centers students attend by year
avg_by_year = []
title = "Average number of centers attended by students per year"
fig_name = "centers_per_student"

for year in xrange(len(num_centers_student)): 
	num_centers_by_year = {}

	w_results.writerow([])
	f = ["Centers attended by each student"] + [x_labels_years[year]]
	w_results.writerow(f)

	student_row = []
	to_write0 = [[] for i in xrange(4)]
	

	f_name = ''.join(f)
	f_csv =  open(f_name +'.csv', 'w+')
	w_f = csv.writer(f_csv)

	w_f.writerow([""] + centers)

	for student, values in num_centers_student[year].items():
		num_centers_by_year.update({student: len(values.keys())})
		student_row.append(student)
		to_write1 = np.zeros(4)
		i = 0
		for c, t in values.items():
			to_write1[centers.index(c)] = t
			to_write0[i].append(c)
			i += 1
		while i < 3: 
			i += 1
			to_write0[i].append("")
		w_f.writerow([student] + list(to_write1))

	w_results.writerow(student_row)

	for row in to_write0: 
		w_results.writerow(row)

	avg_by_year.append(np.average(num_centers_by_year.values()))
	
	# for each year, will want to create with students as rows, centers as columns,
	# and time spent as values


	
graphics.reg_bar_chart(avg_by_year, x_labels_years, title, figname)

w_results.writerow([])
w_results.writerow([title + " (only for students who attended at least one center)"])
w_results.writerow(x_labels_years)
w_results.writerow(avg_by_year)

	






