#Compare 2 readings from RPi
import csv

unique_mac = []
rpi_list = []
rpi2_list = []
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

#read first RPi AP readings
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
                        new_ap = AP(gps_time,time_capt,mac,ssid,sec,rssi,ch,manuf,ap_type,lat,lng)
                        rpi_list.append(new_ap)
		i += 1
		
#read second RPi AP readings
i = 0			
with open('gtn_list.csv','rb') as csvfile:
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
                        new_ap = AP(gps_time,time_capt,mac,ssid,sec,rssi,ch,manuf,ap_type,lat,lng)
                        rpi2_list.append(new_ap)
                i += 1

common_index = []
for rpi in rpi_list:
	for rpi2 in rpi2_list:
                #get common APs in both list
		if rpi.mac == rpi2.mac:
			common_list.append(rpi)
			#remember bssid so we can remove them in rpi/rpi2_list
			common_index.append(rpi.mac)

#remove common aps found in both list to make a list of unique APs for each list
for i in range(len(common_index)):
	for rpi in rpi_list:
		if common_index[i] == rpi.mac:
			rpi_list.remove(rpi)
			break
	for rpi in rpi2_list:
		if common_index[i] == rpi.mac:
			rpi2_list.remove(rpi)
			break

#print final data in csv file
print "Common APs: " + str(len(common_list))
print "Unique 1st List: " + str(len(rpi_list))
print "Unique 2nd List: " + str(len(rpi2_list))
with open('trikexgtn.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	
	##write common aps
	write_file.writerow(["Common",str(len(common_list))])
	write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
	for item in common_list:
		write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	

	#write unique for first file
	write_file.writerow(["Trike",str(len(rpi_list))])
	write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
	for item in rpi_list:
		write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	

	#write unique for second file
	write_file.writerow(["Night",str(len(rpi2_list))])
	write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
	for item in rpi2_list:
		write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])
		
