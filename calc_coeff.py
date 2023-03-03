#!/usr/local/bin/python3

import sys
if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x, not Python 2. Run with the 'python3' command\n")
    exit(1)

import csv
import functools
import argparse

parser = argparse.ArgumentParser(description='Process GA DOE Attendence Files')
parser.add_argument("filename", type=str,
                    help="display a square of a given number")
parser.add_argument('src_quarter', metavar='src_quarter', type=int, 
                    help='which source quarter data line to use')
parser.add_argument('dst_quarter', metavar='dst_quarter', type=int, 
                    help='which destination quarter data line to use')
parser.add_argument('transitions_to_average', metavar='transitions_to_average', type=int, 
                    help='how many transitions to average')
parser.add_argument('--stdfile', action=argparse.BooleanOptionalAction)
parser.add_argument('--historicalprojections', action=argparse.BooleanOptionalAction)
args = parser.parse_args()

debug = False

if debug: print(args.filename, args.src_quarter, args.dst_quarter, args.transitions_to_average,args.stdfile)
schoolfileName = args.filename
schoolfile = open(schoolfileName, 'r')
csv = csv.reader(schoolfile, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
d = dict()
for row in csv: 
  if debug: print(row)
  
  yr = int(row[2])
  qtr = int(row[3])
  sd =  d.get(yr,dict())
  
  sd[qtr] = row
  d[yr]  = sd

if debug: print(d)

for (yr) in d.keys():
    if debug: print(yr)

    transitions_to_average = args.transitions_to_average ## this is kinda fuzzy, people sometimes mean they used 8 years of history, when taking a 7 year average. Sometimes they mean they used 7 years of history, making a 6 year average
    
    dataAvailable = True
    for yrOff in range(transitions_to_average):
      if d.get(yr-yrOff-1) == None:
        dataAvailable = False
        break
    if not dataAvailable:
      continue
        
    survival_rates_from_grade = dict()
    sum_of_srfg = dict()
    for backtrack in reversed(range(transitions_to_average)):

      seg_src = args.src_quarter
      seg_dst = args.dst_quarter
      
      src_yr = yr-backtrack-1
      dst_yr = yr-backtrack

      KINDER_OFFSET = 6
      TOTAL_OFFSET = len(d[dst_yr][seg_dst])-1
      grades_dst = d[dst_yr][seg_dst][KINDER_OFFSET:-1]
      grades_src = d[src_yr][seg_src][KINDER_OFFSET:-1]
      if args.stdfile:
        KINDER_OFFSET = 7
        TOTAL_OFFSET = 5
        grades_dst = d[dst_yr][seg_dst][KINDER_OFFSET:]
        grades_src = d[src_yr][seg_src][KINDER_OFFSET:]
      

        

      for offset in range(len(grades_src)-1):

        use_pct_diff = False
        #calculate via percentage of difference
        if use_pct_diff:
          old_grade = int(grades_src[offset])
          new_grade = int(grades_dst[offset+1])
          delta =  float(new_grade-old_grade)
          frac =  1.0 + (delta/(old_grade))

        #calculate via straight ratio
        else: 
          old_grade = int(grades_src[offset])
          new_grade = int(grades_dst[offset+1])
          delta =  float(new_grade-old_grade)
          if not old_grade == 0:
            frac =  new_grade/old_grade
          else:
            frac = 0
          
  
        if debug: print("{}_{}:{}->{}_{}:{}  leaving grade {} {}{}%".format(src_yr,offset,old_grade, dst_yr,offset+1,new_grade, offset,use_pct_diff,frac*100))
        sum_of_srfg[offset] = survival_rates_from_grade.get(offset,0.0)+frac
        avg_frac_comp = frac/transitions_to_average
        survival_rates_from_grade[offset] = survival_rates_from_grade.get(offset,0.0)+avg_frac_comp
      
   

    #print("For year ending {}, {} year avg cohort survival rates from grade ({}):".format(yr,number_of_years_of_history_to_use,schoolfileName))
    finYear = len(d[yr][1])-8
   
    surv_rates = [str(n) for n in list(survival_rates_from_grade.values())]
    useAvgRatesNotUsingPreDiv = False
    if useAvgRatesNotUsingPreDiv:
      surv_rates = [str(n/transitions_to_average) for n in list(survival_rates_from_grade.values())]

    print("{} yr acsr| For Period Ending with Progression to {}-{} School year: {}|q{}->q{}|{}|{}|{}".format(transitions_to_average,yr-1,yr,schoolfileName,seg_src, seg_dst,use_pct_diff, "KK->1:through:{}->{}".format(finYear-1,finYear), ","+",".join(surv_rates)))
    if (args.historicalprojections and yr <= 2017 and int(d[yr][1][KINDER_OFFSET]) > 0):
      #find set of kindergardeners for period to simulate
      start_fyr= yr
      projecting_over = [ yr+1, yr+2, yr+3, yr+4, yr+5]
      kinders = [d[data_yr][1][KINDER_OFFSET] for data_yr in projecting_over]
      preks =  [int(d[data_yr][1][KINDER_OFFSET-1]) for data_yr in projecting_over]
      actual_totals = [d[data_yr][1][TOTAL_OFFSET] for data_yr in projecting_over]
      
     
      start_year_cohorts = d[start_fyr][1][KINDER_OFFSET:]

      print("QQ {}".format(args.filename))
      print("QQ Projecting using SM basic method treating FY{} as actual data start year and using actual kinders ({}) for fiscal years {}-{}".format(start_fyr,kinders,projecting_over[0], projecting_over[-1]))
      print("QQ coeffs used = {}".format(",".join(surv_rates)))
      description = "actual {}-{}".format(start_fyr-1, start_fyr)
      cohorts = start_year_cohorts
      ptotal = str(functools.reduce(lambda a,b: int(a)+int(b), cohorts[0:len(cohorts)-1]))
      cohorts[len(cohorts)-1] = ptotal
      print("QQ {}: {}".format(description, ",".join(cohorts)))

      for proj_year_index in range(len(projecting_over)):
        proj_year = projecting_over[proj_year_index]
        description = "proj.  {}-{}".format(proj_year-1, proj_year)
        last_yr_cohort = cohorts.copy()
        cohorts[0] = int(kinders[proj_year_index])
        for index in range (1,len(cohorts)-1):
          rate = float(surv_rates[index-1])
          lastyr = float(last_yr_cohort[index-1])
          # print([rate,lastyr,index])
          cohorts[index] = int(round(float(lastyr) * rate ,0))
        ptotal = functools.reduce(lambda a,b: a+b, cohorts[:-1])
        cohorts[len(cohorts)-1] = ptotal
        at = float(actual_totals[proj_year_index]) - preks[proj_year_index]
        raw_err = float(ptotal-at)/float(at)
        err =  round(raw_err*100.0,1)
        err_desc = "overestimate"
        if err < 0.0: 
          err_desc = "underestimate"
          err = 0.0 - err
        print("QQ {}: {} (Actual total (disr prek): {} [SM CPR method is a ^{} of^{}%^] re={}".format(description, ",".join([str(int(i)) for i in cohorts]),actual_totals[proj_year_index],err_desc, err, raw_err))
      
