import json
import csv
import os
import pytz
from datetime import datetime


manila_tz = pytz.timezone("Asia/Manila")

def to_Manila_timezone(time):
    utc_time = datetime.strptime(time, "%Y-%m-%dT%H:%M:%S.000Z")
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(manila_tz)
    local_time = datetime.strftime(local_time,"%Y-%m-%d, %I:%M:%S %p")
    return str(local_time)

def main():    
    with open('search.json') as data_wigle:
        data1 = json.load(data_wigle)

    with open('search2.json') as data_wigle:
        data2 = json.load(data_wigle)

    with open('search3.json') as data_wigle:
        data3 = json.load(data_wigle)
        
    with open('ap_list.csv','wb') as csvfile:
        write_file = csv.writer(csvfile, delimiter = ',')
        write_file.writerow(["SSID","Net ID","TriLat","TriLong","Encryption","Type","Trans ID","First Time","Last Time","Last Updt"])

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

        ##write to file data from search2.json
        for ap in data2['results']:
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

        ##write to file data from search3.json
        for ap in data3['results']:
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

if __name__ == main:
    main()
