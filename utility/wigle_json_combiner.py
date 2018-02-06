##This reads json results from wigle website then puts them in single csv file
import json
import csv
import os
import re
import pytz
from datetime import datetime


manila_tz = pytz.timezone("Asia/Manila")

def to_Manila_timezone(time):
    utc_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.000Z")
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(manila_tz)
    local_time = datetime.strftime(local_time,"%Y-%m-%d, %I:%M:%S %p")
    return str(local_time)

def is_search(s):
        return re.match("search[0-9]+.json", s)
def get_search_number(s):
        return int(s[6:])

#look for all search.json files in the directory given
searches = [s for s in os.listdir('C:/wamp64/www/gmaps/teachersvill/wigledb') if is_search(s)]

#loop through all search.json files and write/append them to the output file
i = 0
for s in searches:
    print s
    with open(s) as data_wigle:
        data1 = json.load(data_wigle)
        
    with open('ap_list.csv','ab+') as csvfile:
        write_file = csv.writer(csvfile, delimiter = ',')
        if i == 0:
            write_file.writerow(["SSID","Net ID","TriLat","TriLong","Encryption","Type","Trans ID","First Time","Last Time","Last Updt"])
        i += 1    
        ##write to file data from search.json
        for ap in data1['results']:
            ssid =  str(ap['ssid'])
            netid =  str(ap['netid'])
            trilat = str(ap['trilat'])
            trilong = str(ap['trilong'])
            enc = str(ap['encryption'])
            ap_type = str(ap['type'])
            transid = str(ap['transid'])
            ftime = str(ap['firsttime'])
            ftime = to_Manila_timezone(ftime)
            ltime = str(ap['lasttime'])
            ltime = to_Manila_timezone(ltime)
            lupdt = str(ap['lastupdt'])
            lupdt = to_Manila_timezone(lupdt)
            write_file.writerow([ssid, netid, trilat, trilong, enc, ap_type, transid, ftime, ltime, lupdt])
