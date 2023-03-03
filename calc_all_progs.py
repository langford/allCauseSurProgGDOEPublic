#!/usr/local/bin/python3

import sys
if sys.version_info < (3, 0):
    print("Sorry, requires Python 3.x, not Python 2. Run with the 'python3' command\n")
    exit(1)



import os 
import csv 
dirls = os.listdir("./eachschool")

print(dirls)
def readMap():
  fn = 'progmap.csv'
  file = open(fn, 'r')
  print("opening file: {}".format(fn))
  csvfile = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
  dictionary = dict()
  for line in csvfile:
    print(line)
    dictionary[line[0]]=line[1]
  return dictionary
  
 
progressionMap = readMap()
print(progressionMap)
print("endprogmap")
addDict = dict()
for each in dirls:
  if not each.endswith("csv"):
    continue
  #print(each)
  name = each.split(".")[0].split("school_")[1]
  #print(name)
  if progressionMap.get(name):
    toAdd = addDict.get(progressionMap[name],[])
    toAdd += [name]
    addDict[progressionMap[name]] = toAdd
    print("{} is in progmap: {}, {}".format(name, progressionMap[name], toAdd))


for k in addDict.keys():
  print("Expanding {}",addDict[k])
  for item in addDict[k]:
    if addDict.get(item):
      print("DEPENDENCY: {} {}".format(item, k))
      addDict[k]+=addDict[item]

for destinationSchool in addDict.keys():
  yearInfo = dict()
  print("{} flows from->{}".format(destinationSchool,addDict[destinationSchool]))
  for filename in addDict[destinationSchool]+[destinationSchool]:
   print(filename)
   with open("./eachschool/school_{}.csv".format(filename)) as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in reader:
      report = line[0]
      toAdd = yearInfo.get(report,[])
      toAdd += [line]
      yearInfo[report] = toAdd
  print(yearInfo)
  print("Adding up {}".format(destinationSchool))
  periodList = list(yearInfo.keys())
  periodList.sort()
  result = []
  title = "Feeders for and {}".format(destinationSchool)
  feederResults = []
  for reportPeriod in periodList:
    print("showing period: {} which has {} schools with info".format(reportPeriod,len(yearInfo[reportPeriod])))

    result = yearInfo[reportPeriod][0][0:4]
    result += [title]
    datalen = len(yearInfo[reportPeriod][0])
    print("leader: {}".format(result))
    print(datalen)
    for i in range(5,datalen):
      sum = 0
      for schoolIdx in range(len(yearInfo[reportPeriod])):
        value = int(yearInfo[reportPeriod][schoolIdx][i])
        print("Found {} at yearInfo[{}][{}][{}] in {}".format(value, reportPeriod, schoolIdx,i,yearInfo[reportPeriod][schoolIdx][4]))
        print("   {}".format(yearInfo[reportPeriod][schoolIdx]))
        sum += value
      result += ["{}".format(sum)]
      print(result)
    print(result)
    feederResults += [result]
    
    file = open("./feeder_data/feederAndSchool_{}.csv".format(destinationSchool), 'w+')
    writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for line in feederResults:
        writer.writerow(line)
  

    

