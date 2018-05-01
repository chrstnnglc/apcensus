#This filters the master list of APs if an AP reading is in Teacher's Village East
#This will also compute the persistence of each AP
#Output files will be:
#   persist_bflist.csv -> persistence of bflog_readings.txt
#   tve_list.csv -> list of APs found in Teachers Village East
#   persist_tve.csv -> persistence of APs in Teachers Village East

import math
import csv
from latlng_distance import *
import geopy.distance
import datetime

class Boxes:
    def __init__(self, north=None, south=None, east=None, west=None): 
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.unique_macs = []
        self.ap_list = []
        self.time_spent = 0
        self.speed = 0
        self.traversal = 0
        self.avg_speed = 0

class AP:
    def __init__(self, gps_time=None, time_capt=None, mac=None, ssid=None, sec=None, rssi=None, ch=None, manuf=None, ap_type=None,lat=None, lng=None):
        self.gps_time = gps_time
        self.time_capt = time_capt
	self.mac = mac
	self.ssid = ssid
	self.security = sec
	self.rssi = rssi
	self.channel = ch
	self.manuf = manuf
	self.ap_type = ap_type
	self.lat = lat
        self.lng = lng
        self.persistence = 0
        self.dates_seen = ""
        
class BF:
    def __init__(self, gps_date=None, mac=None, lat=None, lng=None):
        self.gps_date = gps_date
        self.mac = mac
        self.lat = lat
        self.lng = lng
        self.persistence = 0
        self.dates_seen = ""

    def add_persistence(self):
        self.persistence += 1

    def add_dates_seen(self,date_string):
        if date_string not in self.dates_seen:
            self.dates_seen += date_string + ", "


class GPS:
   def __init__(self, gps_date=None, time_capt=None, lat=None, lng=None):
       self.gps_date = gps_date
       self.time_capt = time_capt
       self.lat = lat
       self.lng = lng

def round_off_time(time_string):
    if int(time_string[20]) >= 5:
        output_time = time_string[:19]
        output_time = datetime.datetime.strptime(output_time,"%Y-%m-%d %H:%M:%S")
        output_time = output_time + datetime.timedelta(seconds=1) #add 1 to seconds
    else:
        output_time = time_string[:19]
        output_time = datetime.datetime.strptime(output_time,"%Y-%m-%d %H:%M:%S")

    return output_time
    
#this list will contain all of the BFlog readings
bf_readings = []

#initialize the BF readings
bf_file = open("bflog_readings.txt","r")
for line in bf_file:
    parsed = line.split()
    gps_date = parsed[0]
    mac = parsed[3]
    coords = parsed[8]
    coords = coords[1:]
    coords = coords.split(",")
    coords[1] = coords[1].strip()
    lat = float(coords[0])
    lng = float(coords[1])
    #only consider the readings with gps data
    if lat != 0.000000 and lng != 0.000000:
        new_ap = BF(gps_date,mac,lat,lng)
        bf_readings.append(new_ap)
bf_file.close()

#this list will contain all of the class box that we have
box_list = []

#these will be the bounds of the first box
north = 14.647254
south = LatCoordDistance(north,50)
west = 121.057193
east = LngCoordDistance(north,west,50)

#initialize the boxes
for i in range(0,14):
    if i != 0:
        north = south
        south = LatCoordDistance(north,50)
        west = 121.057193
        east = LngCoordDistance(north,west,50)
    for j in range(0,9):
        if j != 0:
            west = east
            east = LngCoordDistance(north,west,50)
        #we try to imitate the shape of tve with our boxes
        if (i >=7 and j==0):
            continue
        if (i >= 10 and j >= 6):
            continue
        if (i == 0 and j >= 2):
            continue
        new_box = Boxes(north,south,east,west)

        for ap in bf_readings:
            #check if AP is within the box bounds
            if ((ap.lat <= new_box.north) and (ap.lat >= new_box.south)) and ((ap.lng <= new_box.east) and (ap.lng >= new_box.west)):
                #check if AP is in unique aps in that box. We only add those who are not in unique so we avoid adding persistence when we encounter multiple readings in a single passing on that box
                if ap.mac not in new_box.unique_macs:
                    new_box.unique_macs.append(ap.mac)
                    #search if AP is already in the list of aps found in that box
                    in_ap_list = 0
                    for ap_found in new_box.ap_list:
                        #if yes, we just add 1 to persistence of that AP
                        if ap.mac == ap_found.mac:
                            in_ap_list = 1
                            ap_found.add_persistence()
                            ap_found.add_dates_seen(ap.gps_date[0:10])
                    #if not,add 1 to persistence of new found AP before putting it to list of aps found in the box
                    if in_ap_list == 0:
                        ap.add_persistence()
                        ap.add_dates_seen(ap.gps_date[0:10])
                        new_box.ap_list.append(ap)
            #if found AP is not within box, it means that the tricycle passed through the box already so we reset unique APs
            else:
                new_box.unique_macs = []


        box_list.append(new_box)
        
#make a csv file for BF persistence
with open("persist_bflist.csv","wb") as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    number = 0
    #write_file.writerow(["Total No. of APs", str(len(unique_macs))])
    for box in box_list:
        write_file.writerow(["Box no.", "Total APs"])
        write_file.writerow([str(number), str(len(box.ap_list))])
        write_file.writerow(["MAC", "Persistence", "Dates Seen"])
        for ap in box.ap_list:
            write_file.writerow([ap.mac, str(ap.persistence), ap.dates_seen[:-1]])
        number += 1
        write_file.writerow([""])


#this list will contain all of the AP readings
ap_readings = []
#this will contain all of the APs in TVE
tve_list = []

#initialize the AP readings
ap_file = open("master_list.txt","r")
for line in ap_file:
    parsed = line.split("|")
    gps_time = parsed[0].strip()
    time_capt = parsed[1].strip()
    mac = parsed[2].strip()
    ssid = parsed[3].strip()
    sec = parsed[4].strip()
    rssi = parsed[5].strip()
    ch = parsed[6].strip()
    manuf = parsed[7].strip()
    ap_type = parsed[8].strip()
    lat = float(parsed[9].strip())
    lng = float(parsed[10].strip())
    #only consider the readings with gps data
    if lat != 0.000000 and lng != 0.000000:
        new_ap = AP(gps_time,time_capt,mac,ssid,sec,rssi,ch,manuf,ap_type,lat,lng)
        #We will find this AP in the list of APs found per box. We will add all persistence of the AP per box, and also the dates seen
        for box in box_list:
            for ap in box.ap_list:
                if ap.mac == new_ap.mac:
                    new_ap.persistence += ap.persistence
                    dates = ap.dates_seen.split(",")
                    for date_string in dates:
                        if date_string not in new_ap.dates_seen:
                            if date_string != " ":
                                    new_ap.dates_seen += date_string.strip() + ", " 
        ap_readings.append(new_ap)
ap_file.close()

#we reset our box list
box_list = []

#these will be the bounds of the first box
north = 14.647254
south = LatCoordDistance(north,50)
west = 121.057193
east = LngCoordDistance(north,west,50)

#initialize the boxes again. This time we add all persistence to compute for the
#persistence of unique list of APs
for i in range(0,14):
    if i != 0:
        north = south
        south = LatCoordDistance(north,50)
        west = 121.057193
        east = LngCoordDistance(north,west,50)
    for j in range(0,9):
        if j != 0:
            west = east
            east = LngCoordDistance(north,west,50)
        ##we try to imitate the shape of tve with our boxes
        if (i >=7 and j==0):
            continue
        if (i >= 10 and j >= 6):
            continue
        if (i == 0 and j >= 2):
            continue
        new_box = Boxes(north,south,east,west)
        for ap in ap_readings:
            #check if AP is within the box bounds
            if ((ap.lat <= new_box.north) and (ap.lat >= new_box.south)) and ((ap.lng <= new_box.east) and (ap.lng >= new_box.west)):
                new_box.ap_list.append(ap)
                tve_list.append(ap)
        box_list.append(new_box)

#we will now compute for the time spent, average speed, no. of traversals of boxes
gps_list = []   #this list will contain gps readings
gps_file = open("master_gps.txt","r")   #open gps file
for line in gps_file:
    parsed = line.split("|")
    gps_date = parsed[0].strip()
    time_capt = parsed[1].strip()
    lat = float(parsed[2].strip())
    lng = float(parsed[3].strip())
    new_gps = GPS(gps_date,time_capt,lat,lng)
    gps_list.append(new_gps)
gps_file.close()

for box in box_list:
    first_time = 0
    for i in range(0,len(gps_list)):
        if ((gps_list[i].lat <= box.north) and (gps_list[i].lat >= box.south)) and ((gps_list[i].lng <= box.east) and (gps_list[i].lng >= box.west)):
            if first_time == 0:
                start_time = round_off_time(gps_list[i].time_capt)
                first_time = 1
                start_point = (gps_list[i].lat,gps_list[i].lng)
        else:
            if first_time == 1:
                end_time = round_off_time(gps_list[i-1].time_capt)
                time_spent = (end_time - start_time).seconds
                box.time_spent += time_spent
                first_time = 0
                end_point = (gps_list[i-1].lat,gps_list[i-1].lng)
                
                distance =  geopy.distance.vincenty(start_point, end_point).m
                if time_spent != 0:
                    speed = (distance/time_spent) * 3.6   #3.6 to convert from m/s to km/hr
                    box.speed += speed
                    box.traversal += 1

#make a csv file containing information of Boxes
with open("box_info.csv","wb") as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["Box No.","Total AP","Time Spent","Avg Speed","Traversal"])
    number = 0
    for box in box_list:
        #compute for average speed first
        if box.traversal != 0:
            box.avg_speed = box.speed / box.traversal

        write_file.writerow([str(number),str(len(box.ap_list)),str(box.time_spent),str(box.avg_speed),str(box.traversal)])
        number += 1

#make a csv file of APs in TVE
with open("tve_list.csv","wb") as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in tve_list:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	

#make a csv file for TVE persistence
with open("persist_tve.csv","wb") as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    number = 0
    write_file.writerow(["Total No. of APs", str(len(tve_list))])
    for box in box_list:
        write_file.writerow(["Box no.", "Total APs"])
        write_file.writerow([str(number), str(len(box.ap_list))])
        write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude","Persistence","Dates Seen"])
        for item in box.ap_list:
            write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng),str(item.persistence),str(item.dates_seen)])	
        number += 1
        write_file.writerow([""])