#!/usr/bin/python


"""
Author: Janine Heiser
Date: Feb 12 2014
CS290T
Purpose: 
This script can be used to analyze data in the 2012 Presidential Campaign,
available from ftp://ftp.fec.gov/FEC/2012/pas212.zipt - data dictionary is at
http://www.fec.gov/finance/disclosure/metadata/DataDictionaryContributionstoCandidates.shtml
"""

import fileinput
import csv
from decimal import Decimal

def filemeread_totals (filename, total): 
    candidates = []
    amounts = []
    mystuff = []
   # candidate_dic = dict{}
    cnt = 0 
    dc={}
    with open(filename, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter='|')
        for row in spamreader:
            amounts.append(float(row[14]))
            candidates.append(row[16])
            total += float(row[14])
            if not (row[16] in dc):
                dc[row[16]] = [int(row[14])]
            else: 
                mymoney =  dc[row[16]]
                myval = int(row[14])
                mymoney.append(myval)
                dc[row[16]] = mymoney
    mystuff.append(amounts)
    mystuff.append(candidates)
    mystuff.append(dc)
    return mystuff

        
def mymin(contribs):
    min_contribs = sorted(contribs, key=Decimal)   
    return min_contribs[0]

def mymax(contribs):
    max_contribs = sorted(contribs, key=Decimal, reverse=True)       
    return max_contribs[0]

def mymean(contribs):
    mean_contribs = sum(contribs) * 1.0 / len(contribs)
    return  mean_contribs

def mymedian(contribs):
    sortz = sorted(contribs)
    lengthz = len(contribs)
    if not lengthz % 2:
        return (sortz[lengthz / 2] + sortz[lengthz / 2 - 1]) / 2.0
    return sortz[lengthz / 2]

def mystddev(contribs):
    meancontrib = mymean(contribs)
    variance = map(lambda x: (x - meancontrib)**2, contribs)
    avgvar = mymean(variance)
    import math
    standard_deviation = math.sqrt(mymean(variance))
    return standard_deviation

def myzscore(mean_of_pop, std_dev_of_pop, mean_candidate):
    myz = (mean_candidate - mean_of_pop)/std_dev_of_pop
    return myz

def minmax_normalize(value,minz,maxz):
    """Takes a donation amount and returns a normalized value between 0-1. The
    normilzation should use the min and max amounts from the full dataset"""
    mynorms = (Decimal(value) - Decimal(minz))/(Decimal(maxz)-Decimal(minz))
    return round(mynorms,6)


################main####################################

####get the general info for dataset
total = 0.0
filename = 'data/itpas2.txt'
filestuff = filemeread_totals (filename, total)
contribs = filestuff[0]
total = round(sum(contribs),3)
candidates = filestuff[1]
mincontrib =  round(mymin(contribs),3)
maxcontrib =  round(mymax(contribs),3)
meancontrib = round(mymean(contribs),3)
mediancontrib = round(mymedian(contribs),3)
stddevcontrib = round(mystddev(contribs),3)

###get info for individual candidates
all_candidates = []
dc = filestuff[2]
dc_good = dc.items()
for c in dc_good: 
    mycandidate = []
    myc = c[0]
    ind_candidate = myc
    myc_contribs = c[1]
    mycandidate.append("Candidate: " +  ind_candidate)
    mysum = sum(myc_contribs)
    mycandidate.append( " Total: %s" % str(round(mysum,3)))
    mycandidate.append(" Minimum:  %s" % round(mymin(myc_contribs),3))
    mycandidate.append(" Maximum:  %s" % round(mymax(myc_contribs),3))
    candidate_mean = mymean(myc_contribs)
    mycandidate.append(" Mean: %s" %  round(candidate_mean, 3))
    mycandidate.append(" Median: %s" % round(mymedian(myc_contribs),3))
    mycandidate.append(" Standard Deviation: %s" % round(mystddev(myc_contribs),3))
    mycandidate.append(" Z-Score: %s" % round(myzscore(meancontrib, stddevcontrib, candidate_mean),3))
    final_candidate = ",".join( mycandidate)
    all_candidates.append(final_candidate)

print "####Stats for individual candidates####"
for cdz in all_candidates:
    print cdz

####print out all candidate information
print "####Stats for ALL candidates####"
print "Total: %s" % total
print "Minimum:  %s" % mincontrib
print "Maximum:  %s" % maxcontrib
print "Mean: %s" % meancontrib  
print "Median: %s" % mediancontrib
# square root can be calculated with N**0.5
print "Standard Deviation: %s" % stddevcontrib 
##### Normalize some sample values
#x = [2500, 50, 250, 35, 8, 100, 19]
print "Min-max normalized values: %r" % map((lambda x:  minmax_normalize(x, mincontrib, maxcontrib)),  [2500, 50, 250, 35, 8, 100, 19])
##### Comma separated list of unique candidate ID numbers
print "Total Number of Candidates: " 
candidates2 = set(filestuff[1])
print len(candidates2)
    






