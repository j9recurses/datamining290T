#!/usr/bin/python
###Janine Heiser
##i290T
##2/26/2014


"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv
from decimal import Decimal

(
    CMTE_ID, AMNDT_IND, RPT_TP, TRANSACTION_PGI, IMAGE_NUM, TRANSACTION_TP,
    ENTITY_TP, NAME, CITY, STATE, ZIP_CODE, EMPLOYER, OCCUPATION,
    TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID, CAND_ID, TRAN_ID, FILE_NUM,
    MEMO_CD, MEMO_TEXT, SUB_ID
) = range(22)

CANDIDATES = {
    'P80003338': 'Obama',
    'P80003353': 'Romney',
}


###generally we need to: 
##you would be calculating a gini for each zip code and multiply that by its weight across all zips.  
##do this for each zip and sum all the weighted ginis, and it should be a single value. 
#so we calculate the obama vs romney gini for each zip code, multiply that by #
# of donations in that zipcode / # of total donations in all zipcodes), and then add? 

############### Set up variables
# TODO: declare datastructures

from collections import *

def getgini(list_vals):
  sorted_list = sorted(list_vals)
  height, area = 0, 0
  for value in sorted_list:
    height += value
    area += height - value / 2.
  fair_area = height * len(list_vals) / 2
  return (fair_area - area) / fair_area
  

cand_dict = defaultdict(int)
mydict = defaultdict(list)
total_cnt = 0
obamacnt = []
rommeycnt = []
mystuff = []

###
# TODO: calculate the values below:
gini = 0  # current Gini Index using candidate name as the class
split_gini = 0  # weighted average of the Gini Indexes using candidate names, split up by zip code
##/

############### Read through files

for row in csv.reader(fileinput.input(), delimiter='|'):
    candidate_id = row[CAND_ID]
    if candidate_id not in CANDIDATES:
        continue    
    candidate_name = CANDIDATES[candidate_id]
    zipcode = row[ZIP_CODE]
    ##create a tuple with zip and candidate and append to a list, will use a default dict to extract later
    mystuff.append(( candidate_name , zipcode))
    total_cnt = total_cnt + 1 

##here use the cool properties of default dict. For weighted gini- Basically, load each zip as a dictionary key. 
#if it doesn't exist in the dict and create a list of the candidate names for the zip.
## If the zip does exist as key, just append the candidate name to zip list of candidates. 
for s,v in mystuff:
    if v in mydict:
       coolval = mydict[v]
       coolval.append(s)
       mydict[v] = coolval
    if v not in mydict:
        mydict[v] = [s]
    ##now lets grab the stuff we need to the general gini, which is just the candidate
    ##for every instance of a candidate we see, increment by 1 
    if s in cand_dict:
        mycand_val = cand_dict[s]
        mycand_val = mycand_val + 1
        cand_dict[s] =  mycand_val
    if s not in cand_dict:
        cand_dict[s] = 1 


##code below is for the weighted zip code gini

for k,v in mydict.iteritems():  
    ##now lets use the default dict again to sum up the number of donations per zip
    freq = defaultdict(int)
    for candy in v:
        freq[candy] += 1
    zipcodelist = []
    ##now put the freqs in a list and get the number per zip
   ##how to access default dict on index? 
    totalzips = 0
    for m,n in freq.iteritems(): 
        zipcodelist.append(n)
        totalzips = totalzips + n
     ###now we can run the gini function for each zip
    if len(zipcodelist) != 1:
        mycoolgini = getgini(zipcodelist)
    ##if there only is 1 candidate that peeps donated in the zipcode, set gini to 1:
    if len(zipcodelist) == 1:
        mycoolgini = 1
#so we calculate the obama vs romney gini for each zip code, above. 
#now  we multiple the gini for the zip * (# of donations in that zipcode / # of total donations in all zipcodes) 
##and then add to the split_gini
    ginizipratio = float(totalzips) / float(total_cnt)
    wtgini = mycoolgini * ginizipratio
    #print zipcodelist
    #print wtgini
    split_gini = split_gini +  wtgini


##code below is for the non-weigthed gini:
reg_gini = []
for q,r in cand_dict.iteritems(): 
    reg_gini.append(r)
gini = getgini(reg_gini)

print "#####OUTPUT RESULTS##########"
print "Gini Index: %s" % gini
print "Gini Index after split: %s" % split_gini
