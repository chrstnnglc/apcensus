import math
import csv
class Boxes:
    def __init__(self, north=None, south=None, east=None, west=None): 
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.unique_macs = []
        self.ap_list = []

class AP:
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

#Computes for the latitude distance        
def LatCoordDistance(lat,offset):
    R = float(6378137)
    rad_lat_offset = offset/R
    new_lat = (lat - rad_lat_offset * 180/math.pi);
    return round(new_lat,6)


#Computes for the longitude distance
def LngCoordDistance(lat,lng,offset):
    R = float(6378137)
    rad_lng_offset =  offset/(R*math.cos(math.pi/180*lat))
    new_lng = (lng + rad_lng_offset * 180/math.pi)
    return round(new_lng,6);

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
        new_box = Boxes(north,south,east,west)
        box_list.append(new_box)

#this list will contain all of the AP readings
ap_readings = []
#this list will contain unique aps in the whole area
unique_macs = []

#initialize the AP readings
ap_file = open("ap_readings.txt","r")
for line in ap_file:
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
        new_ap = AP(gps_date,mac,lat,lng)
        ap_readings.append(new_ap)
ap_file.close()

#get ap persistence algo
for box in box_list:
    for ap in ap_readings:
        #check if AP is within the box bounds
        if ((ap.lat <= box.north) and (ap.lat >= box.south)) and ((ap.lng <= box.east) and (ap.lng >= box.west)):
            if ap.mac not in unique_macs:
                unique_macs.append(ap.mac)
            #check if AP is in unique aps in that box. We only add those who are not in unique so we avoid adding persistence when we encounter multiple readings in a single passing on that box
            if ap.mac not in box.unique_macs:
                box.unique_macs.append(ap.mac)
                #search if AP is already in the list of aps found in that box
                in_ap_list = 0
                for ap_found in box.ap_list:
                    #if yes, we just add 1 to persistence of that AP
                    if ap.mac == ap_found.mac:
                        in_ap_list = 1
                        ap_found.add_persistence()
                        ap_found.add_dates_seen(ap.gps_date[0:10])
                #if not,add 1 to persistence of new found AP before putting it to list of aps found in the box
                if in_ap_list == 0:
                    ap.add_persistence()
                    ap.add_dates_seen(ap.gps_date[0:10])
                    box.ap_list.append(ap)
        #if found AP is not within box, it means that the tricycle passed through the box already so we reset unique APs
        else:
            box.unique_macs = []

print str(len(unique_macs))
          
#make a csv file for persistence
with open("persist_mlist.csv","wb") as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    number = 0
    write_file.writerow(["Total No. of APs", str(len(unique_macs))])
    for box in box_list:
        write_file.writerow(["Box no.", "Total APs"])
        write_file.writerow([str(number), str(len(box.ap_list))])
        write_file.writerow(["MAC", "Persistence", "Dates Seen"])
        for ap in box.ap_list:
            write_file.writerow([ap.mac, str(ap.persistence), ap.dates_seen[:-1]])
        number += 1
        write_file.writerow([""])
