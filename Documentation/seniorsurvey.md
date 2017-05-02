## Notes on merging senior survey files:

Note that the way I did this was probably not the best, and took a lot of time. I definitely acknowledge there might be a better way to merge the files. ** 

### Tutorial on merging data files:
http://www.d.umn.edu/~mcoleman/tutorials/spss/merge.html

I would definitely create a separate copy of the file, and not overwrite the original trend file.

*Important:* When you do this, there will probably be a lot of excluded variables. In order to deal with this, I renamed all of the excluded variables in the following format: “var” —> “var16” (for year 2017 it would be “var” —> “var17”, etc). 
You can choose the format but I recommend being consistent in how you rename across all variables so that you can find them easily in the data file. 

*Note:* Instead of using the GUI to rename and merge (as described in the tutorial) you can also use SPSS syntax — this will probably be much quicker and painless. You can see the merge syntax output from 2016 to copy / modify in the Drive folder “Senior Surveys / Trends / Cleaning and Combining Files”. It is saved as “2006-2016_mergesyntax.sps”. 

Once you have merged the files, you then have to go through all of the excluded variables and do the following (all in SPSS syntax): 
(1) check if they have the same value encodings as the variable with the previous years encoding. e.g. some variables might have 0/1 mapped to No/Yes, while their newer counterparts might have the same variable labels mapped to 1/2. If the encodings are different, recode. 
(2) combine the variables across the years 
(3) delete the single year version of the variable

Start by combining the two year variables together, so that you can just do a simple if statement to combine over the years  (e.g. do if year = 2017 … ) 

I have the syntax I used to merge the files saved in the drive under Senior Surveys / Trends / Cleaning and Combining Files as “2016cleaning_final.sps”. You can look at that to get ideas of how to merge the variables together.  



