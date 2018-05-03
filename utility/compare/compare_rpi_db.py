#Compare RPi AP readings and Wigle DB APs
import csv
import operator
rpi_list = []
db_list = []
common_list = []

class AP:
        def __init__(self, gps_time=None, time_capt=None, mac=None, ssid=None, sec=None, rssi=None, ch=None, manuf=None, ap_type=None,lat=None, lng=None,):
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
		self.last_updt = ""     #will be equal to wigle db last updt if same ap/mac

class WDB:
        def __init__(self, last_updt=None, last_time=None, mac=None, ssid=None, sec=None, ch=None,lat=None, lng=None):
                self.last_updt = last_updt
                self.last_time = last_time
                self.mac = mac
                self.ssid = ssid
                self.security = sec
                self.channel = ch
                self.lat = lat
                self.lng = lng
		
#read RPi trace
i = 0		
with open('tve_list.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in reader:
                if i >= 1:   #ignore first line
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
                        new_ap = AP(gps_time,time_capt,mac,ssid,sec,rssi,ch,manuf,ap_type,lat,lng)
                        rpi_list.append(new_ap)
                i += 1
		
#read Wigle DB trace
i = 0			
with open('traversed_tve_wdb.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in reader:
                if i >= 1:   #ignore first line
                        last_updt = line[0]
                        last_time = line[1]
                        mac = line[2]
                        ssid = line[3]
                        sec = line[4]
                        ch = line[5]
                        lat = line[6]
                        lng = line[7]
                        new_ap = WDB(last_updt, last_time, mac, ssid, sec, ch, lat, lng)
                        db_list.append(new_ap)
                i += 1

#Compare RPi and Wigle DB        
common_index = []		
for rpi in rpi_list:
	for wdb in db_list:
		#if same ang bssid, ibig sabihin nakita sa both device. Add data of rpi to wigle reading then put to common list
		if rpi.mac == wdb.mac:
			#we add wdb.last_updt value to rpi attributes for presenation purposes
                        rpi.last_updt = wdb.last_updt
                        common_list.append(rpi)
			#remember bssid so we can remove them in rpi/db_list
			common_index.append(rpi.mac)

#remove common aps in rpi and db list
for i in range(len(common_index)):
	for ap in rpi_list:
		if common_index[i] == ap.mac:
			rpi_list.remove(ap)
			break
	for ap in db_list:
		if common_index[i] == ap.mac:
			db_list.remove(ap)
			break
#we sort our lists wrt last_updt value in Wigle DB for presentation purposes
common_list.sort(key=operator.attrgetter('last_updt'),reverse=True)
db_list.sort(key=operator.attrgetter('last_updt'),reverse=True)

#print final data in csv file			
print "Common APs: " + str(len(common_list))
print "Unique RPi: " + str(len(rpi_list))
print "Unique Wigle DB: " + str(len(db_list))
with open('trikexwdb.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	#write common aps
	write_file.writerow(["Common",str(len(common_list))])
	write_file.writerow(["GPS Time","LastUpdt(WDB)","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in common_list:
                write_file.writerow([str(item.gps_time),str(item.last_updt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	

	#write unique aps in rpi
	write_file.writerow([" "])
	write_file.writerow(["RPi",str(len(rpi_list))])
	write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in rpi_list:
                write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	
	
	#write unique aps in db
	write_file.writerow([" "])
	write_file.writerow(["Wigle DB", str(len(db_list))])
	write_file.writerow(["Last Updt","Last Time","MAC","SSID","Encryption","Channel","Latitude","Longitude"])
        for item in db_list:
                write_file.writerow([str(item.last_updt),str(item.last_time),str(item.mac),str(item.ssid),str(item.security),str(item.channel),str(item.lat),str(item.lng)])
    
