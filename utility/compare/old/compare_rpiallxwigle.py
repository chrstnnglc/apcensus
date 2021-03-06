##THIS COMPARES all csv readings from RPi (1,6,11 and 1-13), Wigle, and Wigle DB
import csv

unique_bssid = []
rpi2_list = []
rpi_list = []
common_list = []
wigle_list = []
site_list = []
rpi_wigle_common = []
common_all = []
class AP:
	def __init__(self, bssid=None, ssid=None, channel=None,enc=None):
		self.bssid = bssid
		self.ssid = ssid
		self.channel = channel
		self.enc = enc
		self.r_channel = ""
		self.r_enc = ""
		self.last = ""
		
		self.avg_rssi = 0
		self.sum_rssi = 0
		self.num_readings = 0
		self.r_avg_rssi = 0
		
	def add_num_packets(self):
		self.num_readings += 1
		
	def compute_avg_rssi(self):				
		self.avg_rssi = self.sum_rssi / self.num_readings

##read Rpi 1-13 trace
i = 0		
with open('trace.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i > 1:		##ignore first line
			
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]
			
			new_ap = AP(bssid,ssid,channel,enc)
			rpi2_list.append(new_ap)
		i += 1

print "APs in 1-13: " + str(len(rpi2_list))		

##read RPi 1,6,11 trace
i = 0			
with open('z_trace.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i != 0:		##ignore first line
			
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]
			
			new_ap = AP(bssid,ssid,channel,enc)
			rpi_list.append(new_ap)
		i += 1
		
print "APs in 1,6,11: " + str(len(rpi_list))

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

##compare 1-13 and 1,6,11
rpi_index = []
rpi2_index = []		
for rpi2 in rpi2_list:
	for rpi in rpi_list:
		##if same ang bssid, ibig sabihin nakita sa both device. Add data of rpi to wigle reading then put to common list
		if rpi2.bssid == rpi.bssid:
			common_list.append(rpi2)
			##remember bssid so we can remove them in rpi/wigle_list
			rpi2_index.append(rpi2.bssid)
			rpi_index.append(rpi.bssid)

##compare common in rpi with wigle
wigle_index = []		
for wigle in wigle_list:
	for common in common_list:
		##if same ang bssid, ibig sabihin nakita sa both device. Add data of rpi to wigle reading then put to common list
		if wigle.bssid == common.bssid:
			wigle.r_channel = common.channel
			wigle.r_avg_rssi = common.r_avg_rssi
			wigle.r_enc = common.enc
			rpi_wigle_common.append(wigle)
			##remember bssid so we can remove them in rpi/wigle_list
			
			
##compare wigle with 1,6,11
wx1611 = 0
for wigle in wigle_list:
	for rpi in rpi_list:
		##if same ang bssid, ibig sabihin nakita sa both device. Add data of rpi to wigle reading then put to common list
		if wigle.bssid == rpi.bssid:
        		wx1611 += 1
			wigle.r_channel = rpi.channel
			wigle.r_avg_rssi = rpi.r_avg_rssi
			wigle.r_enc = rpi.enc
			##remember bssid so we can remove them in rpi/wigle_list
			rpi_index.append(rpi.bssid)
			wigle_index.append(wigle.bssid)
			
##compare wigle with 1-13
wx113 = 0
for wigle in wigle_list:
	for rpi in rpi2_list:
		##if same ang bssid, ibig sabihin nakita sa both device. Add data of rpi to wigle reading then put to common list
		if wigle.bssid == rpi.bssid:
                        wx113 += 1
			wigle.r_channel = rpi.channel
			wigle.r_avg_rssi = rpi.r_avg_rssi
			wigle.r_enc = rpi.enc
			##remember bssid so we can remove them in rpi/wigle_list
			rpi2_index.append(rpi.bssid)
			wigle_index.append(wigle.bssid)

			
##remove not unique ap in wigle list
for i in range(len(wigle_index)):
        for wigle in wigle_list:
		if wigle_index[i] == wigle.bssid:
			wigle_list.remove(wigle)
			break
##remove not unique ap in 1-13 list
for i in range(len(rpi2_index)):
	for rpi2 in rpi2_list:
		if rpi2_index[i] == rpi2.bssid:
			rpi2_list.remove(rpi2)
			break
##remove not unique ap in 1,6,11 list
for i in range(len(rpi_index)):
	for rpi in rpi_list:
		if rpi_index[i] == rpi.bssid:
			rpi_list.remove(rpi)
			break

##print final data in csv file
print "------------------------------------"
print "Common APs between 1-13 and 1,6,11: " + str(len(common_list))
print "Common APs between 1,6,11 and WiGLE: " + str(wx1611)
print "Common APs between 1-13 and WiGLE: " + str(wx113)
print "Common APs in all: " + str(len(rpi_wigle_common))
print "------------------------------------"
print "Unique 1-13: " + str(len(rpi2_list))
print "Unique 1,6,11: " + str(len(rpi_list))
print "Unique WiGLE: " + str(len(wigle_list))

with open('rpiallxwigle.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	
	##write common aps
	write_file.writerow(["Common in ALL",str(len(rpi_wigle_common))])
	write_file.writerow(["BSSID","SSID","Wigle-Encryption","RPi-Encryption","Wigle-Channel","RPi-Channel","Wigle Avg RSSI","RPi Avg RSSI"])
	for item in common_all:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.r_enc),str(item.channel),str(item.r_channel),str(item.avg_rssi),str(item.r_avg_rssi)])
	
	##write unique aps in wigle
	write_file.writerow([" "])
	write_file.writerow(["WiGLE Unique",str(len(wigle_list))])
	write_file.writerow(["BSSID","SSID","Wigle-Encryption","Wigle-Channel","Wigle Avg RSSI"])
	for item in wigle_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel),str(item.avg_rssi)])
		
	##write unique aps in rpi
	write_file.writerow([" "])
	write_file.writerow(["1,6,11 Unique", str(len(rpi_list))])
	write_file.writerow(["BSSID","SSID","RPi-Encryption","RPi-Channel","RPi Avg RSSI"])
	for item in rpi_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel),str(item.r_avg_rssi)])

	##write unique aps in rpi
	write_file.writerow([" "])
	write_file.writerow(["1-13 Unique", str(len(rpi2_list))])
	write_file.writerow(["BSSID","SSID","RPi-Encryption","RPi-Channel","RPi Avg RSSI"])
	for item in rpi2_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel),str(item.r_avg_rssi)])
	
