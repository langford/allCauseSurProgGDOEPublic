#!/usr/local/bin/python3

import sys
if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x, not Python 2. Run with the 'python3' command\n")
    exit(1)


import csv
import traceback 
import re
from pprint import pprint
import json 
SPARKID = "0116"
MESID = "1664"
MLID = "2564"
APSID = " System Total for Atlanta Public Schools"
HOWARD_ID = "1563"
HH_ID = "2062"

def openSchoolFile(suffix, dir="./"):
  fn = dir + 'school_{}.csv'.format(suffix)
  file = open(fn, 'w')
  print("opening file: {}".format(fn))
  csvfile = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  return csvfile

def openSchoolJsonFile(suffix, dir="./"):
  fn = dir + 'school_{}.json'.format(suffix)
  file = open(fn, 'w')

  return file



filedict = dict()
jsonfiledict = dict()

debug = False
def tryint(s):
  try:
    return int(s)
  except Exception:
    return s

def convert_to_ints_if_possible(row):
  
  result = [tryint(s) for s in  row]
  print("Conv({}) -> {}".format(row,result))
  return result

def filename_safe_school_desc(desc):

  return re.sub('[^A-Za-z0-9]+', '', re.sub(' ','_', desc))


  
   
school_ids = sorted([SPARKID, MESID, MLID, HH_ID, HOWARD_ID,APSID])
print("School IDS{}".format(school_ids))
all_data = dict()
def process_file(fn,yr,qtr):
  print("Processing file {}".format(fn))
  prelude = []

  
  with open(fn) as csvfile:
    next(csvfile)
    next(csvfile)
    date = next(csvfile).strip()[1:-1]
    act_date,fydate = date.split('(')
    fydate = fydate[:-1]
    next(csvfile)
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    prelude = [fydate,act_date] + [yr,qtr]
    aggregateElimData = [0,0,0,0,0,0,0,0]
    listOfAggregateElimData = []
    howardCounts = [0,0,0,0]
    aggCount=0
    valid_rows = []
    next(csvfile)
    next(csvfile)
    
    for row in spamreader:
      print("row:{}".format(row))

      mrow = []

      if len(row) < 3:
       print("too small{}".format(row))
       continue


      school_desc = row[2]


      school_filename = filename_safe_school_desc(school_desc)
      data_so_far_this_school = all_data.get(school_filename,dict())
      data_this_year = data_so_far_this_school.get(yr,dict())


      std_file = filedict.get(school_filename,None)
      if std_file == None:
        print("No file yet for " + school_filename)
        std_file = openSchoolFile(school_filename,dir = './eachschool/')
        filedict[school_filename] = std_file
 
      mrow_std = prelude + [school_desc] + row[3:] 
      mrow_std_numeric =  prelude + [school_desc] + convert_to_ints_if_possible(row[3:]) 
      data_this_year[qtr] = mrow_std_numeric
      data_so_far_this_school[yr] = data_this_year  
      all_data[school_filename] = data_so_far_this_school

      print("writing: {} ".format(mrow_std_numeric))
      std_file.writerow(mrow_std_numeric)

     
      print("storing {}".format(data_so_far_this_school))
       
 

     
         
for i in range(24):
   year = i+2008
   fnPattern = "past/FTE Enrollment by Grade Fiscal Year{}-{} Data Report.csv"
   fn1 = fnPattern.format(year,1)
   fn3 = fnPattern.format(year,3)
   try:
     process_file(fn1,year,1)
   except Exception:
    print("exception")
    pass
   try:
     process_file(fn3,year,3)
   except Exception:
    print("exception")
    pass


json_file = openSchoolJsonFile("__all_data",dir = './eachschool_js/')
encoded_json = json.dumps(all_data,indent=2, sort_keys=True)
json_file.write(encoded_json)
json_file.close()
print("options:")
print("----------")
sortedKeys = all_data.keys()
sortedKeys = sorted(sortedKeys)
for schoolName in sortedKeys:
  schoolData = all_data[schoolName]
  keys = schoolData.keys()
 
  schoolNamePretty = ""
  for k in keys:
    
    for i in schoolData[k]:
      schoolNamePretty = schoolData[k][i][4]
  json_file = openSchoolJsonFile(schoolName,dir = './eachschool_js/')
  encoded_json = json.dumps({k:schoolData})
  json_file.write(encoded_json)  
  json_file.close()
  print('<option value="{}">{}</option>'.format(schoolName, schoolNamePretty))

  


