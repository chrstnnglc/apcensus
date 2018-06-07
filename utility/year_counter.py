import csv

count_2013 = 0
count_2014 = 0
count_2015 = 0
count_2016 = 0
count_2017 = 0
count_2018 = 0

i = 0
with open('comp3-unique_wdb.csv','rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in reader:
        if i == 0:  #since files containing Last Updt column is not consistent in order, we do this
            if "Updt" in line[0]:
                index = 0
            if "Updt" in line[1]:
                index = 1
        if i >= 1:
            last_updt = line[index]
            last_updt = last_updt[:4]
            
            if last_updt == "2013":
                count_2013 += 1
            elif last_updt == "2014":
                count_2014 += 1
            elif last_updt == "2015":
                count_2015 += 1
            elif last_updt == "2016":
                count_2016 += 1
            elif last_updt == "2017":
                count_2017 += 1
            elif last_updt == "2018":
                count_2018 += 1
        i += 1

print "Total AP: " + str(count_2013 + count_2014 + count_2015 + count_2016 + count_2017 + count_2018)
print "2013: " + str(count_2013)
print "2014: " + str(count_2014)
print "2015: " + str(count_2015)
print "2016: " + str(count_2016)
print "2017: " + str(count_2017)
print "2018: " + str(count_2018)
