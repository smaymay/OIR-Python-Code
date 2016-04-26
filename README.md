# OIR-Python-Code

Repository for python code written by WC OIR interns. 
Upload only general scripts that may be modified for other
uses, and obviously don't upload anything that could
be confidential.

Projects should be added as sub-folders within the repository
and their general purposes should be documented in this README.

Projects:

1. cohortanalysis was used originally used to assist in merging separate 
surveys sent to the same group of students over the course of four years.  
Typical workflow: Take a bunch of files that map emails (or some other
variable that is unique to every student in the school) to reponse id's
that are unique with in a given file.  Make sure they are in csv form
(you can use the helper methods in utils to do this or add your own). 
Put all these csv files in a directory, and make sure they are in the 
same format (e.g. col 0 is universal id; col 1 is response id). 
Run the find_cohort.py script. Run the organize_results script from
utils.py on the output, and then run merge_syntax on the output of 
that. (Future task: Put all of these methods into one easy to use 
program :) )

2. tutorvisitsanalysis is a script that looks tutor data, extracts
information to answer preliminary research questions, and creates 
graphics accordingly.  Also saves results of some research questions
to CSV files. 

3. analyzecomments contains scripts to analyze open ended responses / 
comments that might be part of a survey. analyzecomments.py takes in a 
csv file, where each row is a comment, and writes a table to a new csv 
file where each row is a comment, each column is a noun, and the cells are 
a boolean (1, 0) indicating 1: the noun appears in the comment, or 0: the 
noun does not appear in the  comment.  Only nouns that appear in > 
threshold number of comments are included.
