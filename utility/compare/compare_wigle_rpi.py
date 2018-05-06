#Compare RPi and Wigle App readings
import csv
rpi_list = []
wapp_list = []
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

class WA:
        def __init__(self, time_capt=None, mac=None, ssid=None, sec=None, rssi=None, ch=None,lat=None, lng=None):
                self.time_capt = time_capt
                self.mac = mac
                self.ssid = ssid
                self.sec = sec
                self.rssi = rssi
                self.ch = ch
                self.lat = lat
                self.lng = lng
        

#read RPi trace
i = 0		
with open('gtn_list.csv','rb') as csvfile:
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

#read Wigle App unique trace
i = 0
with open('gtn_wigle_unique.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in reader:
                if i >= 1:   #ignore first line
                        time_capt = line[0]
                        mac = line[1]
                        ssid = line[2]
                        sec = line[3]
                        rssi = line[4]
                        ch = line[5]
                        lat = line[6]
                        lng = line[7]
                        new_ap = WA(time_capt,mac,ssid,sec,rssi,ch,lat,lng)
                        wapp_list.append(new_ap)
                i += 1

#compare RPi and Wigle App trace
common_index = []
for rpi in rpi_list:
        for wapp in wapp_list:
                if rpi.mac == wapp.mac:
                        common_list.append(rpi)  
                        common_index.append(rpi.mac)

#remove common aps in rpi and wapp list
for i in range(len(common_index)):
        for ap in rpi_list:
                if common_index[i] == ap.mac:
                        rpi_list.remove(ap)
                        break
        for ap in wapp_list:
                if common_index[i] == ap.mac:
			wapp_list.remove(ap)
			break

#print final data in csv file			
print "Common APs: " + str(len(common_list))
print "Unique RPi: " + str(len(rpi_list))
print "Unique Wigle App: " + str(len(wapp_list))

#create a csv file
with open('gtnxwigle.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	#write common aps
	write_file.writerow(["Common",str(len(common_list))])
	write_file.writerow(["GPS Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in common_list:
                write_file.writerow([str(item.gps_time),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	

	#write unique aps in rpi
	write_file.writerow([" "])
	write_file.writerow(["RPi",str(len(rpi_list))])
	write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in rpi_list:
                write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	
	
	#write unique aps in db
	write_file.writerow([" "])
	write_file.writerow(["Wigle App", str(len(wapp_list))])
	write_file.writerow(["First Seen","MAC","SSID","Encryption","RSSI","Channel","Latitude","Longitude"])
        for item in wapp_list:
                write_file.writerow([str(item.time_capt),str(item.mac),str(item.ssid),str(item.sec),str(item.rssi),str(item.ch),str(item.lat),str(item.lng)])

