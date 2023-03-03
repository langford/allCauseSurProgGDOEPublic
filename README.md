# All Cause Progression Rate Generator

## Intro

My name is Michael Langford. I built this tool to attempt to better understand
projections published by Atlanta Public Schools during the
Facilities Master Planning process they use when resize schools and they rezone
them.

This tool uses public data. If you wish to use private data, then you can, but
you need to reformat it to match the public data format provided by the state 
website and put it in the appropriate place before running one of the tools. It
is highly encouraged that third parties using this tool who choose to modify the
base data when projecting also publish the source data used to derive their 
projections.

The essential function of this tool is to derive an "all-cause cohort survivial
rate" for grade to grade progression through the APS school system. This concept 
is abbreviated by one tool in its output as "acsr". This concept is better
introduced first by an example which I'll go through in the Theory Appendix, but
in short, it's the value you multiply a school's student count in a grade by to project out
next year's student count.

There is defintely a bit of historical cruft sitting around in a few of the
python files: producing code for internal use vs publication is a different
beast, and it was time to get these tools over to others at this point instead
of worrying someone somewhere might think I'm a bit messy at times. That said,
they do pretty simple things on a step by step basis that should be verifiable
with a check in excel, so hopefully, they are useful still.  

Several other tools
related to/using this data are not included which I have privately still, but will get them to
you in the future if you'd like them. 

## Tool Data

This tool set uses two pieces of data: 

Downloaded data files from the Georgia Department
of Education site (See the Obtaining State FTE Data section below). I've encluded some
recent years but feel free to download fresh ones to ensure I've not
accidentally or intentionally changed one or more of them. 

A mapping file (progmap.csv) you make which says which schools feed into which other schools.
Currently, as of March 3 2023, that file only lists the Midtown cluster, but I'm
happy to expand it with help to cover most/all other schools if I get a human
readable explanation of which schools feed to which other schools or you can
give it a go.


## Running the tools

### import_historical.py

This tool reconfigures state data into a more usable format

After obtaining and filling in the correct data for the two tool data file
types, you first import the historical data into a series of files by school.
You do this by running the following command (if you only have python3 on your
computer, you may just need to type "python" instead of "python3"):

    python3 import_historical.py

If it worked, a *very large* pile of text you can largely ignore will go by.
There will be a lot of html with option tags in it with the school names
prepended with their IDs at the end of that output. The items in the quotes
after the value= are what you put in the mapping file.

If the tool worked, you'll see the state files from the "past" directory which
have been ingested into the tool, then output
on a per school basis. This has happended in two folders: eachschool, and
eachschool_js. The eachschool folder is csv files and the other is json files. 

### calc_all_progs.py

This compiles the state data according to the progmap.csv file to fill in the
previous grades for all schools in the mapping file. This allows for easy
determination of acsr/progression rates for middle schools and high schools. 

This tool is run like this: 

    python3 calc_all_progs.py

It will output into the feeder_data folder several csv file similar to those in the
eachschool folder. There will be one csv file per school that is on the "right
side" of the mapping file. That is, every school you tell the software should
have a school fed into it will have that schools attendence data summed up and
added to the school it feeds to. This allows progression rates/acsr to be
determined for these schools using the *calc_coeff.py* tool just like you can
with elementary schools. 


### calc_coeff.py

This tool generates progression rates from the resliced files in the eachschool
directory. You can specify which quarters, how many years, and several other
parameters. To duplicate the first quarter to first quarter progression rates
recently used in the FMP around VHE, you should use command lines like the
following:

    python3 calc_coeff.py --stdfile eachschool/school_1664MorningsideElementarySchool.csv 1 1 7

This will output a series of progression rates for the period ending in each
year specified. The last line of this specific command looks like this: 

    7 yr acsr| For Period Ending with Progression to 2022-2023 School year: eachschool/school_1664MorningsideElementarySchool.csv|q1->q1|False|KK->1:through:11->12|,1.038637638148624,0.9750383105446044,0.9719986328209664,0.9558032193093113,0.9383134254396333,0.0,0.0,0.0,0.0,0.0,0.0,0.0

I know that's *really really dense*, so I suggest you paste that into *excel* to
get started. It's formatted so if you realy want, you can use as a separator in
excel the "|" characters
to get each of the first half of the lines into fields, but usually, you can
just leave that pile of info alone, and use the ",". If you scan through that
big ol line to the numbers after the "11->12|" part, those are your 7 year all
cause survival rates for each of kk->01 through 11->12 if that school has data
for that. 

So for Morningside: 

1.038637638148624,0.9750383105446044,0.9719986328209664,0.9558032193093113,0.9383134254396333

Should work to generate projections for the next couple years given a source of
kindergarten projections. 

### Checking the tools/other projection coefficients

Now since these tools *don't actually have a source of kindergarten data* for
the current time spam, they can only do forward projections themselves for
elementary schools over past data to check the correctness of previous results.
It does not use projected kindergarteners, just the historical ones though. The
tools correctly direguard Pre-K from the school totals.

To do that, run the tool like this: 

   python3 calc_coeff.py --stdfile eachschool/school_1664MorningsideElementarySchool.csv 1 1 7 --historicalprojections

You'll see the output has several lines which start with QQ and grade the
accuracy of estimating with survival rates 

If you want to specify the end year of the 5 year test you put one more paramter
on there: 

  python3 calc_coeff.py --stdfile eachschool/school_1664MorningsideElementarySchool.csv 1 1 7 --historicalprojections --historicalprojectionsendyear 2022

That said, for *high schools*, the kindergarten projection data doesn't really
matter. After running the *calc_all_progs.py*

Now, for high schools and middle schools, just like needing a source of
kindergartener data for elementary schools, you need a source of data for 

### Getting Coefficients for high schools and middle schools

Since high schools and middle schools need to have their feeder schools attached
to them to do similar progression/cohort survival analysis, that's what
*calc_all_progs.py* did for you. It essentially made csv files of the same
format as the elementary school ones in the eachschool directory, except they
have all the school that feed into them in there by grade summed up. This allows
you to do do cohort progression on them!

    python3 calc_coeff.py --stdfile feeder_data/feederAndSchool_4560MidtownHighSchool.csv 1 1 7 

This will spit out the progresion rates for the high school given the feeders of
Howard and Centennial. I know Centennial only has a percentage zoned that way: The goal
of using public data for the projections (and the reality of only having it)
made the tool need to work that way. Removing Centennial from the projections is
as easy as deleting that line from the progmap.csv file if you want to see the
coefficients it generates there. 


### Generating projections into the future with calc_projection.py

The calc_coeff.py script already would do projections on past data to check
accuracy of this method of projecting data. Since I had already implemented this
kind of projection, it wasn't a huge deal to make it work for the future too.
While I'd recently used these scripts to generate coefficients for Midtown High
School, I'd personally used excel to project into the future. Since I was going
to the trouble of writing up these tools and sending them over, I just made a
copy of the calc_coeff program and modfified it slightly to also do future
projections. This is a very new script, taking the coeffiecents from calc_coeff
and using those in excel is possibly more reliable right now. 

Basic operation: 

     python3 calc_projection.py --stdfile feeder_data/feederAndSchool_4560MidtownHighSchool.csv 1 1 7 

This will *still* generate coefficients just like the calc_coeff script will. 

Generate Projections: 

     python3 calc_projection.py --stdfile feeder_data/feederAndSchool_4560MidtownHighSchool.csv 1 1 7 --ffstart 2023 --ffend 2033 --fastforward

This says to use the last real school population for the school (and it's feeder
schools) and extrapolate out. By default , it just repeatedly uses the
kindergarten data from the last year. It starts from the ff start year (which
has to be a year with real data) then projects from there. --fastforward is what
tells it to do it at all, the ffstart and ffend years are the years to project
over. 

Among other things it will print out the total kinds in KK-5, 6-8 and 9-12. This
allows you to pick up the middle school or highschool total enrollment. (Example
years)

Partial Output from a HS

   FF actual 202X-202Y: 509,558,508,524,494,473,467,432,470,474,410,358,360,6037  ['KK-5', '6-8', '9-12'] (note sums do not include Pre-K)
   FF proj.  202Z-202Q: 509,518,544,491,502,470,456,453,414,478,432,400,347,6014  ['3034', '1323', '1657']

Partial Output from a MS (note how the HS grades are empty)

  FF actual 202X-202Y: 412,460,421,440,396,383,367,348,404,0,0,0,0,3631  ['KK-5', '6-8', '9-12'] (note sums do not include Pre-K)
  FF proj.  202Z-202Q: 412,417,446,405,423,376,373,359,338,0,0,0,0,3549  ['2479', '1070', '0']


I hope this tool is useful is quickly obtaining projections in the future for
you. 

Additionally, you can supply the kindergarteners for future years as well: 

    python3 calc_projection.py --stdfile feeder_data/feederAndSchool_4560MidtownHighSchool.csv 1 1 7 --ffstart 2023 --ffend 2033 --fastforward --ffkindercounts "1, 2, 3, 4 ,5 ,6 ,7 , 8,9,10"

(Obviously these are not realistic counts here, but I wanted it to be clear). 

7 yr acsr| For Period Ending with Progression to 2022-2023 School year: feeder_data/feederAndSchool_4560MidtownHighSchool.csv|q1->q1|False|KK->1:through:11->12|,1.017930071477035,0.9756325067714591,0.9670767040945649,0.9586716148234482,0.9515952206893967,0.9638676013774881,0.9708629297548358,0.9589649558464176,1.016910461032702,0.9114594580189302,0.9754589888317757,0.9693133508646159
2024 2033
FF feeder_data/feederAndSchool_4560MidtownHighSchool.csv
FF Projecting using SM basic method treating FY2023 as actual data start year and using kinder supplied from command line  ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) for fiscal years 2024-2033
FF coeffs used = 1.017930071477035,0.9756325067714591,0.9670767040945649,0.9586716148234482,0.9515952206893967,0.9638676013774881,0.9708629297548358,0.9589649558464176,1.016910461032702,0.9114594580189302,0.9754589888317757,0.9693133508646159
FF actual 2022-2023: 509,558,508,524,494,473,467,432,470,474,410,358,360,6037  ['KK-5', '6-8', '9-12'] (note sums do not include Pre-K)
FF proj.  2023-2024: 1,518,544,491,502,470,456,453,414,478,432,400,347,5506  ['2526', '1323', '1657']
FF proj.  2024-2025: 2,1,505,526,471,478,453,443,434,421,436,421,388,4979  ['1983', '1330', '1666']
FF proj.  2025-2026: 3,2,1,488,504,448,461,440,425,441,384,425,408,4430  ['1446', '1326', '1658']
FF proj.  2026-2027: 4,3,2,1,468,480,432,448,422,432,402,375,412,3881  ['958', '1302', '1621']
FF proj.  2027-2028: 5,4,3,2,1,445,463,419,430,429,394,392,363,3350  ['460', '1312', '1578']
FF proj.  2028-2029: 6,5,4,3,2,1,429,450,402,437,391,384,380,2894  ['21', '1281', '1592']
FF proj.  2029-2030: 7,6,5,4,3,2,1,417,432,409,398,381,372,2437  ['27', '850', '1560']
FF proj.  2030-2031: 8,7,6,5,4,3,2,1,400,439,373,388,369,2005  ['33', '403', '1569']
FF proj.  2031-2032: 9,8,7,6,5,4,3,2,1,407,400,364,376,1592  ['39', '6', '1547']
FF proj.  2032-2033: 10,9,8,7,6,5,4,3,2,1,371,390,353,1169  ['45', '9', '1115']


## Configuring/Obtaining Tool Data


### Obtaining State FTE Data

See
https://georgiainsights.gadoe.org/Data-Collections/Documents/FTE%20Resources/FY2023/FTE%20Checklist-GaDOE%202023.pdf
for a description of the processed made to collect the data

To get the actual data, go to
https://georgiainsights.gadoe.org/Pages/DataDownloads.aspx then click "Student
Enrollment By Grade Level (PK-12)" and download all of the reports for each
published
quarter for Atlanta Public Schools, for the past 10 years or so, and put them in the "past" folder. First
select the quarter you want, then the Atlanta Public Schools school district in
the new dropdown that appears. Click "Get Report". This will display the data,
but click "Download \*.csv" then allow your browser to
download the csv file if it asks you if it can. Then put this file in the "past"
folder of this tool. 

I have not tested the tool to see if it works if there are no 3rd quarter data
files present, it may or may not work without them present. 


### Writing the School Mapping

The school mapping is in a file called progmap.csv. This is a list of schools
that end up sending students to other schools. This is used only for an advanced
feature of the toolset (high school projection) and can be disreguarded if you
only care about determining progression rates for elementary schools. 

Let's look at some lines in that file:

    2564MaryLinElementarySchool,1563DavidTHowardMiddleSchool
    1664MorningsideElementarySchool,1563DavidTHowardMiddleSchool
    0116SpringdaleParkElementarySchool,1563DavidTHowardMiddleSchool
    2062TheJohnHopeCharlesWalterHillElementarySchools,1563DavidTHowardMiddleSchool
    9999VirginiaHighlandElementarySchool,1563DavidTHowardMiddleSchool
    1563DavidTHowardMiddleSchool,4560MidtownHighSchool
    0199CentennialPlaceAcademyCharter,4560MidtownHighSchool


Now focusing on one line: 

    2564MaryLinElementarySchool,1563DavidTHowardMiddleSchool

What this says is that "After going to Mary Lin, a percentage/all of the
students will progress to Howard Middle school"

Focusing on another line:

    0199CentennialPlaceAcademyCharter,4560MidtownHighSchool

What this says is that "After going to Centennial, a percentage/all of the
students will progress to Howard Middle school"

How do you get these weird looking ways to express the school name? They will be
reflected in the output of the "import_historical.py" tool, but are essentially
all the non-letter, non-number characters removed from the name shown in the
State FTE files prepended with the schools ID number. (A placeholder ID has been
put in for the new elementary school, Virgina-Highland Elementary, and should be
updated in the future to the real ID). 

I believe I've provided the mappings required to calculate midtown highschool.
If I'm missing some feeder schools, please let me know. I was less sure of the
mappings for many other schools, but if I were to be presented with it in a
human readable format, it would only take a short time for me to adapt it to
match the computer expected format. 

Please be aware: Extraneous spaces at the beginning/end of a school name can
cause the tool to break. You should always "bench check" each high school by
picking one grade at all the schools you know eventually feed into it and check
the output in the 

#### How does the tool deal with changes/rezonings

In a word, it doesn't! I don't have data such as "what percentage of students at
school X live in zone Y" or anything like that, so I can't account for that in
any of these projections. That said, *you* can do that by breaking each school
up into two parts in the "past" folder and in the progmap.csv file.

---

## Tool Usage

After putting many years of past data into the past folder, then, you can run
the first tool "import_historical.py". This tool requires you have a version of
python on your computer greater than 3.0. You must also operate the tool from
the command line. The tool was primarily tested on a mac system, but it will
likely work on a windows computer as well. 



## Theory Appendix

### What is All-Cause Cohort Survival Rate

A fictional school, Mayknot Elementary, in 2005 has the following number of students in the following
grades:

    Kindergarten: 100
    First Grade: 120
    Second Grade: 98
    Third Grade: 83
    Fourth Grade: 93
    Fifth Grade: 103

Therefore in 2005, the school had an enrollment of 597 students. 

If in the year 2006, the school had the following number of students in each
grade:

    Kindergarten: 130
    First Grade: 110
    Second Grade: 117
    Third Grade: 92
    Fourth Grade: 80
    Fifth Grade: 89

It would then have an enrollment of 618 students. 

In modeling, we sometimes call a group of one thing a *cohort*. Now we could
label each grade of students at a school a cohort, for sure, but we could also label a larger group or a
group that's bound by a different definition as a cohort as well. Just as long
as our cohorts don't overlap very much (or better, at all), you can do math on
the progression from one cohort to another over a period of time.  For some
exercises, we could call the entire elementary school a cohort, and that would
be alright. 

Since 2nd graders typically become 3rd graders, you can use the average rate at
which that happens to project future amounts of third graders. This kind of
thing is a *very standard* way school districts tend to project student
enrollment nubmers from year to year. If you think about it, looking at this
kind of thing really does catch "all reasons" for the numeric change, as it's
literally a historical measurement. 

So from the 2005 to the 2006 school year, the "acsr" is 98->92 or 93.877551%. 
That means if we want to predict the 2007 school year's third grade class size,
we might assume it's going to be a similar rate of progression. So, in 2006, the
second grade cohort is 117 students. So 93.877551% * 117 = 109.83673467. 

Now there certainly are some tall kids out there. That's for sure. But
realistically, we've come to a point where we have to make a decision here.
Either there are 109 or 110 students predicted by this method, not 109.83673467
students :D. But that decision aside, you see how that would give a very
reasonable seeming possibility for student enrollment when applied over and
over to make projections of future student counts. This movement from one cohort
to another is called "survival", as it was originally used in overall population
analysis from birth to old age, but people tend to still call it that when this
cohort to cohort progression analysis is used elsewhere. 


It turns out, this method does fairly well and that's why it's used many places to project enrollment for schools across the US and
has been for 70+ years. 

To even out the projections, instead of just using 1 year's grade to grade
progression, you can use the percentage of students who progress across that
threshold over a number of years and average that rate. So you could use a "1
year acsr" to average progression from one year to another, or a "7 year acsr"
to average progression over 7 transitions. This will tend to give more accurate
results which error in a fairly normal distribution (this means most wrong
results will still be close, and really wrong results will be rarer the wronger
they are, on average, no matter if higher or lower).

Now why is it called "All-Cause". Well, that is because it's literally
historical data that is how many people were in each cohort at a specific time.
Unless you go back through the historical data and subtract out grade to grade
changes that match another cause, you cannot simply combine this methodology
with another and get that same normal distribution of accuracy as that cause is
already partially modeled with this rate. This is really a summation of the
effects of students moving into the school, out of the school, being promoted,
being held back, and a few other effects. 

If you have another data source beyond historical per grade attendence values you wish to add to your model, you need a
similar run of historical data of that secondary source and you need to subtract
that other source out of the ACSR source data before calculating coefficients
first. This allows you to then later add that external source in after the fact and still get "largely accurate
results which error in a normal distribution around the likely future results". As an example:

If Mayknot Elementary has a nearby daycare, Morning Glory Daycare, which is very good. Many residents
use it and choose to use its private kindergarten instead of the public school
kindergarten. This ends up causing part of the wierd effect seen in the data where there
are more first graders than there were kindergarteners the previous year. 

From 2005, Mayknot Elementary has: 

    Kindergarten: 100
    First Grade: 120

In 2006

    Kindergarten: 130
    First Grade: 110

But we don't *actually know* why there are 10 more first graders in 2006 than
there are in 2005 until we look. For mass analyis, that would be a lot of extra
work, but if we *did* want to factor in a major change to a single school or two
when projecting, say, that daycare
quadrupling in size, we *could* look (via surveys, enrollment data, registration
data, communication with the daycare under the auspicies of a transfer of
records, etc). 

If we found out with that detailed historical look that we got 11 new first
graders in 2006 who had came to Mayknot Elementary from that daycare, we could
factor that out. 

    K->1st grade acsr without adjustment: 100->110 == 110%

    K->1st grade acsr removing  "Morning Glory's enrollment cause": 100->99 == 99%

Why would you ever do that? How is that useful? Well, if you happen to know that
Morning Glory Elementary quadrupled in size in 2006 you can then adjust the ACSR
down to remove it from the causes that the ACSR is modeling before
multiplying the remaining ACSR then *add in* whatever actual count you project
will come from the school that year. That means if you are fairly certain there
will not be 11, but instead 44 first graders coming in 2007 from Morning Glory's
private kindergarten, then after doing the multiplication step with the acsr
that has had that private kindergarten cause removed, you can add
those 44 students right in.

From 2005, Mayknot Elementary has: 

    Actual Kindergarten: 100
    Actual First Grade: 120

In 2006:

    Actual Kindergarten: 130
    Actual First Grade: 110

Projecting 2007 using data intensive approach which entirely removes cause from
multiplication:

    Projected First Grade cohort after removing the 
      private kindergarteners cause then adding in:  

      (130 * 99%) + 44 = 172.2

Projecting 2007 using simpler approach where only the difference is added:

    Projected First Grade cohort if you just add the
      expected change in without first subtracting it out of the history:  
      
      (130 * 110%) + 33 = 176

Projecting 2007 just adding the projected class of 44 private kindergarteners: 

    Projected First Grade cohort if you just add in the new 
      private kindergarten class without finding out the past 
      private kindergarten contribution:  

      (130 * 110%) + 44 = 187

Why are these different? 
  
  Cohort survival projection methodologies are really a summation of a number of
  factors: Migration in, Migration out, Students failing, previous years
  students having failed, all being simulated out by drawing a straight line
  into the future. You can quite literally see the slope of a graph of each
  cohort is literally the survival rate if you graph them year by year for each cohort. 

  However, that slope is really a sum of each effect being multiplied out (to
  project it's future value) then added together. When you leave a component in
  you happen to be adjusting to a specific amount when you multiply, you end up
  causing error because the "multiplicative" effect of the previous amount is
  kept in even though when you've decided to model it externally. This causes
  overcounting for positive effects, and undercounting for negative effects. 
  That's bad. That's especially likely when the "cause" you're doing this for is
  one that's really a additive factor not truly based on the prior year's cohort size. (Such
  as a new building generating new enrollment instead of a policy change which
  causes more students to pass). 

  Simply though: All-cause survivial rate is about all causes. When you wish to
  independently model a specific cause and add it in after the fact, entirely
  remove that cause to get the cleanest results. 


