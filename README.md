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
introduced first by an example.

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
already partially modeled with this rate. 

If you have another data source you wish to add to your model, you need a
similar run of historical data of that other source and you need to subtract
that other source out of the ACSR before calculating coefficients if you wish to
add that external source in after the fact and still get "largely accurate
results which error in a normal distribution". As an example:

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

But we don't actually *know* why there are 10 more first graders in 2006 than
there are in 2005 until we look. For mass analyis, that would be a lot of extra
work, but if we *did* want to factor in a major change, say, that daycare
quadrupling in size, we *could* look (via surveys, enrollment data, registration
data, communication with the daycare under the auspicies of a transfer of
records, etc). 

If we found out with that detailed historical look that we got 11 new first
graders in 2006 who had came to Mayknot Elementary from that daycare, we could
factor that out. 

K->1st grade acsr without adjustment: 100->110 == 110%

K->1st grade acsr adjusted for removing the cause "Morning Glory's enrollment
cause": 100->99 == 99%

Why would you ever do that? How is that useful? Well, if you happen to know that
Morning Glory Elementary quadrupled in size in 2006 you can then adjust the ACSR down to remove it from the causes before
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

In 2007 using data intensive approach:

  Projected First Grade cohort after removing the private kindergarteners cause then adding in:  
      (130 * 99%) + 44 = 172.2

In 2007 using simpler approach where only the difference is added:

  Projected First Grade cohort if you just add the expected change in without first
  subtracting it out of the history:  
      (130 * 110%) + 33 = 176

In 2007 just adding the projected class of 44 private kindergarteners: 

  Projected First Grade cohort if you just add in the new private kindergarten
  class without finding out the past private kindergarten contribution:  
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
  That's bad. 


