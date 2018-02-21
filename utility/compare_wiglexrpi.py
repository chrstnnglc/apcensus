##THIS COMPARES Wigle readings and RPi readings
import csv

unique_bssid = []
wigle_list = []
rpi_list = []
common_list = []

class AP:
	def __init__(self, bssid=None, ssid=None, channel=None,enc=None):
		self.bssid = bssid
		self.ssid = ssid
		self.channel = channel
		self.enc = enc
		self.r_channel = ""
		self.r_enc = ""
		
		self.avg_rssi = 0
		self.sum_rssi = 0
		self.num_readings = 0
		self.r_avg_rssi = 0
		
	def add_num_packets(self):
		self.num_readings += 1
		
	def compute_avg_rssi(self):				
		self.avg_rssi = self.sum_rssi / self.num_readings
##read Wigle trace
i = 0		
with open('WigleWifi_20180218142909.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i > 1:	##ignore first 2 lines
			
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[4]
			rssi = int(line[5])
			
			if bssid not in unique_bssid:
				unique_bssid.append(bssid)
				new_ap = AP(bssid,ssid,channel,enc)
				new_ap.add_num_packets()
				new_ap.sum_rssi += rssi
				wigle_list.append(new_ap)
			else:
				bssid = line[0]
				rssi = rssi = int(line[5])
				for item in wigle_list:
					if bssid == item.bssid:
						item.add_num_packets()
						item.sum_rssi += rssi
		i += 1
	for item in wigle_list:
		item.compute_avg_rssi()

print "APs in WiGLE: " + str(len(wigle_list))		

##read RPi trace
i = 0			
with open('z_trace.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i != 0:		##ignore first line
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]
			avg_rssi = line[5]
			new_ap = AP(bssid,ssid,channel,enc)
			new_ap.r_avg_rssi = avg_rssi
			rpi_list.append(new_ap)
		i += 1
		
print "APs in RPi: " + str(len(rpi_list))
		
rpi_index = []
wigle_index = []		
for wigle in wigle_list:
	for rpi in rpi_list:
		##if same ang bssid, ibig sabihin nakita sa both device. Add data of rpi to wigle reading then put to common list
		if wigle.bssid == rpi.bssid:
			wigle.r_channel = rpi.channel
			wigle.r_avg_rssi = rpi.r_avg_rssi
			wigle.r_enc = rpi.enc
			common_list.append(wigle)
			##remember bssid so we can remove them in rpi/wigle_list
			wigle_index.append(wigle.bssid)
			rpi_index.append(rpi.bssid)

##remove common aps in wigle and rpi list
for i in range(len(rpi_index)):
	for wigle in wigle_list:
		if wigle_index[i] == wigle.bssid:
			wigle_list.remove(wigle)
			break
	for rpi in rpi_list:
		if rpi_index[i] == rpi.bssid:
			rpi_list.remove(rpi)
			break


##print final data in csv file			
print "Common APs: " + str(len(common_list))
print "Unique WiGLE: " + str(len(wigle_list))
print "Unique RPi: " + str(len(rpi_list))
with open('1611xwigle.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	
	##write common aps
	write_file.writerow(["Common",str(len(common_list))])
	write_file.writerow(["BSSID","SSID","Wigle-Encryption","RPi-Encryption","Wigle-Channel","RPi-Channel","Wigle Avg RSSI","RPi Avg RSSI"])
	for item in common_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.r_enc),str(item.channel),str(item.r_channel),str(item.avg_rssi),str(item.r_avg_rssi)])
	
	##write unique aps in wigle
	write_file.writerow([" "])
	write_file.writerow(["WiGLE Unique",str(len(wigle_list))])
	write_file.writerow(["BSSID","SSID","Wigle-Encryption","Wigle-Channel","Wigle Avg RSSI"])
	for item in wigle_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel),str(item.avg_rssi)])
		
	##write unique aps in rpi
	write_file.writerow([" "])
	write_file.writerow(["RPi Unique", str(len(rpi_list))])
	write_file.writerow(["BSSID","SSID","RPi-Encryption","RPi-Channel","RPi Avg RSSI"])
	for item in rpi_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel),str(item.r_avg_rssi)])
