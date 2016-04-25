# OIR-Python-Code

Repository for python code written by WC OIR interns. 
Upload only general scripts that may be modified for other
uses, and obviously don't upload anything that could
be confidential.

Projects should be added as sub-folders within the repository
and their general purposes should be documented in this README.

Projects:

1. cohortanalysis was used to assist in merging separate surveys
sent to the same group of students over the course of four years. 

2. tutorvisitsanalysis is a script that looks tutor data, extracts
information to answer preliminary research questions, and creates 
graphics accordingly.  Also saves results of some research questions
to CSV files. 

3. analyzecomments contains scripts to analyze open ended responses / 
comments that might be part of a survey. analyzecomments.py takes in a 
csv file, where each row is a comment, and writes a table to a new csv 
file where each row is a comment, each comment is a noun, and the cells are 
a boolean (1, 0) indicating 1: the noun appears in the comment, or 0: the 
noun does not appear in the  comment.  Only nouns that appear in > 
threshold number of comments are included.
