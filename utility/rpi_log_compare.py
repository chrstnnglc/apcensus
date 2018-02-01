##Compares rpi log.csv files
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

##read Wigle trace
i = 0		
with open('trace_01312018.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in reader:
		if i > 1:		##ignore first line
			row = ','.join(row)
			line = row.split(',')
			
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]
			
			new_ap = AP(bssid,ssid,channel,enc)
			wigle_list.append(new_ap)
		i += 1

print "APs in 1-13: " + str(len(wigle_list))		

##read RPi trace
i = 0			
with open('z_trace_01312018.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for row in reader:
		if i != 0:		##ignore first line
			row = ','.join(row)
			line = row.split(',')
			
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]
			
			new_ap = AP(bssid,ssid,channel,enc)
			rpi_list.append(new_ap)
		i += 1
		
print "APs in 1,6,11: " + str(len(rpi_list))
		
rpi_index = []
wigle_index = []		
for wigle in wigle_list:
	for rpi in rpi_list:
		##if same ang bssid, ibig sabihin nakita sa both device. Add data of rpi to wigle reading then put to common list
		if wigle.bssid == rpi.bssid:
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
print "Unique 1-13: " + str(len(wigle_list))
print "Unique 1,6,11: " + str(len(rpi_list))
with open('log_traces_01312018.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	
	##write common aps
	write_file.writerow(["Common",str(len(common_list))])
	write_file.writerow(["BSSID","SSID","Encryption","Channel"])
	for item in common_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])
		
	##write unique for first file
	write_file.writerow(["1-13",str(len(wigle_list))])
	write_file.writerow(["BSSID","SSID","Encryption","Channel"])
	for item in wigle_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])
		
	##write unique for second file
	write_file.writerow(["1,6,11",str(len(rpi_list))])
	write_file.writerow(["BSSID","SSID","Encryption","Channel"])
	for item in rpi_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])
