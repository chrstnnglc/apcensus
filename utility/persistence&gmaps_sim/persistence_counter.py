#This counts the number of Access Points within the persistence ranges:
# 1 to 10, 10 to 20, 20 to 30, 30 to 40, 40 and above

import csv


class AP:
	def __init__(self, gps_time=None, time_capt=None, mac=None, ssid=None, sec=None, rssi=None, ch=None, manuf=None, ap_type=None,lat=None, lng=None, box_num=None, box_time=None, box_speed=None, box_traversal=None, persistence=None, dates_seen=None):
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
		self.box_num = box_num
		self.box_time = box_time
		self.box_speed = box_speed
		self.box_traversal = box_traversal
                self.persistence = persistence
                self.dates_seen = dates_seen
                self.last_updt = ""     #will be equal to wigle db last updt if same ap/mac



ap_list = []
count1 = 0
count2 = 0
cout3 = 0
count4 = 0
count5 = 0
i = 0	
with open('tve_list.csv','rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in reader:
        if i >= 1:		#ignore first line
            gps_time = line[0]
            time_capt = line[1]
            mac = line[2]
            ssid = line[3]
            sec = line[4]
            rssi = line[5]
            ch = line[6]
            manuf = line[7]
            ap_type = line[8]
            lat = line[9]
            lng = line[10]
            box_num = line[11]
            box_time = line[12]
            box_speed = line[13]
            box_traversal = line[14]
            persistence = line[15]
            dates_seen = line[16]
            new_ap = AP(gps_time,time_capt,mac,ssid,sec,rssi,ch,manuf,ap_type,lat,lng,box_num,box_time,box_speed,box_traversal,persistence,dates_seen)
            ap_list.append(new_ap)
	i += 1

for ap in ap_list:
    if int(ap.persistence) >= 1 and int(ap.persistence) <= 10:
        count1 += 1
    elif int(ap.persistence) >= 11 and int(ap.persistence) <= 20:
        count2 += 1
    elif int(ap.persistence) >= 21 and int(ap.persistence) <= 30:
        count3 += 1
    elif int(ap.persistence) >= 31 and int(ap.persistence) <= 40:
        count4 += 1
    elif int(ap.persistence) > 40:
        count5 += 1
        

print "No. of APs with persistence 1 to 10: " + str(count1)
print "No. of APs with persistence 11 to 20: " + str(count2)
print "No. of APs with persistence 21 to 30: " + str(count3)
print "No. of APs with persistence 31 to 40: " + str(count4)
print "No. of APs with persistence above 40: " + str(count5)

