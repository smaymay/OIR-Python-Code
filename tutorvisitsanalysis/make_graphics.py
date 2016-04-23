import numpy as np
import matplotlib.pyplot as plt

__author__ = 'Sarah May'

"""Program to make summary graphics -- mainly intended for results from TutorTrac
data analysis but could probably be generalized to other data. 
These graphics aren't professional enough for deliverables or reports, but they are 
good to generate quick visiual summaries of data. 
"""
colors = ['#A0CFEB', '#002776', '#E8EB6F', '#007A87']

def stacked_bar_chart(vals, legend_labels, x_labels, title, figname):
	"""Creates stacked bar chart from provided data. len(vals) must equal
	len(legend_labels), and each sublist within vals must have same length as 
	len(x_labels). Uses style in accordance with Wellesley College 
	Visual Identity Guidelines"""

	n = len(x_labels)
	ind = np.arange(n)
	width = 0.35

	# initialize y offset
	y_offset = np.array([0.0]*n)

	plts = []
	for row in xrange(len(vals)): 
		p = plt.bar(ind, vals[row], width, bottom=y_offset, color=colors[row%4])
		y_offset = y_offset + vals[row]
		plts.append(p)


	plt.title(title)
	plt.legend((p[0] for p in plts), [l for l in legend_labels], loc=2)
	plt.xticks(ind+width/2., x_labels)
	plt.savefig(figname + ".png")
	plt.close()

def reg_bar_chart(vals, x_labels, title, figname): 
	"""Creates regular bar chart
	"""
	n = len(x_labels)
	ind = np.arange(n)
	width = 0.35

	plt.bar(ind, vals, width, color=colors[2])
	plt.title(title)
	plt.xticks(ind+width/2, x_labels)
	plt.savefig(figname + ".png")
	plt.close()

def pie_chart(vals, legend_labels, title, figname):
	"""Creates a pie chart using style in accordance with Wellesley College
	Visual Identity Guidelines.
	"""
	chart_colors = [colors[i%4] for i in xrange(len(vals))]
	plt.pie(vals, colors=chart_colors, autopct='%1.1f%%',labels=legend_labels)
	plt.title(title)
	plt.savefig(figname + ".png")
	plt.close()

