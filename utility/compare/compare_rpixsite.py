##THIS COMPARES Wigle.csv readings and data from Wigle Site
import csv

unique_bssid = []
rpi_list = []
site_list = []
common_list = []

class AP:
	def __init__(self, bssid=None, ssid=None, channel=None,enc=None):
		self.bssid = bssid
		self.ssid = ssid
		self.channel = channel
		self.enc = enc
		self.enc2 = ""
		self.last = ""
		
##read rpi trace
i = 0		
with open('z_trace.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i != 0:	##ignore first line
			
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]
			
			if bssid not in unique_bssid:
				unique_bssid.append(bssid)
				new_ap = AP(bssid,ssid,channel,enc)
				rpi_list.append(new_ap)
		i += 1

print "APs in Rpi: " + str(len(rpi_list))		

##read Site trace
i = 0			
with open('ap_list.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i != 0:		##ignore first line
			
			ssid = line[0]
			bssid = line[1]
			enc = line[4]
			last = line[9]
			
			new_ap = AP(bssid,ssid,channel,enc)
			new_ap.last = last
			site_list.append(new_ap)
		i += 1
		
print "APs in Wigle Site: " + str(len(site_list))
		
site_index = []
wigle_index = []		
for wigle in rpi_list:
	for site in site_list:
		##if same ang bssid, ibig sabihin nakita sa both device. Add data of rpi to wigle reading then put to common list
		if wigle.bssid.upper() == site.bssid:
			wigle.enc2 = site.enc
			wigle.last = site.last
			common_list.append(wigle)
			##remember bssid so we can remove them in rpi/wigle_list
			wigle_index.append(wigle.bssid)
			site_index.append(site.bssid)

##remove common aps in wigle and rpi list
for i in range(len(site_index)):
	for wigle in rpi_list:
		if wigle_index[i] == wigle.bssid:
			rpi_list.remove(wigle)
			break
	for site in site_list:
		if site_index[i] == site.bssid:
			site_list.remove(site)
			break

##print final data in csv file			
print "Common APs: " + str(len(common_list))
print "Unique Rpi: " + str(len(rpi_list))
print "Unique Site: " + str(len(site_list))
with open('1611xsite.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	
	##write common aps
	write_file.writerow(["Common",str(len(common_list))])
	write_file.writerow(["BSSID","SSID","Encryption","Site-Encryption","Last Update"])
	for item in common_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.enc2),str(item.last)])
	
	##write unique aps in wigle
	write_file.writerow([" "])
	write_file.writerow(["Rpi Unique",str(len(rpi_list))])
	write_file.writerow(["BSSID","SSID","Encryption"])
	for item in rpi_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc)])
		
	##write unique aps in site
	write_file.writerow([" "])
	write_file.writerow(["Wigle Site Unique", str(len(site_list))])
	write_file.writerow(["BSSID","SSID","Site-Encryption","Last Update"])
	for item in site_list:
		write_file.writerow([str(item.bssid).upper(),str(item.ssid),str(item.enc),str(item.last)])
