##THIS COMPARES Wigle.csv readings and data from Wigle Site
import csv

unique_bssid = []
wigle_list = []
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
		
##read Wigle trace
i = 0		
with open('WigleWifi_20180205111451.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i > 1:	##ignore first 2 lines
			
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[4]
			
			if bssid not in unique_bssid:
				unique_bssid.append(bssid)
				new_ap = AP(bssid,ssid,channel,enc)
				wigle_list.append(new_ap)
		i += 1

print "APs in Wigle: " + str(len(wigle_list))		


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
for wigle in wigle_list:
	for site in site_list:
		##if same ang bssid, ibig sabihin nakita sa both device. Add data of rpi to wigle reading then put to common list
		if wigle.bssid.upper() == site.bssid:
			wigle.enc2 = site.enc
			wigle.last = site.last
			common_list.append(wigle)
			##remember bssid so we can remove them in rpi/wigle_list
			wigle_index.append(wigle.bssid)
			site_index.append(site.bssid)

for i in range(len(site_index)):
	for wigle in wigle_list:
		if wigle_index[i] == wigle.bssid:
			wigle_list.remove(wigle)
			break
	for site in site_list:
		if site_index[i] == site.bssid:
			site_list.remove(site)
			break

##print final data in csv file			
print "Common APs: " + str(len(common_list))
print "Unique Wigle: " + str(len(wigle_list))
print "Unique Site: " + str(len(site_list))
with open('wiglexsite.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	
	##write common aps
	write_file.writerow(["Common",str(len(common_list))])
	write_file.writerow(["BSSID","SSID","Wigle-Encryption","Site-Encryption","Last Update"])
	for item in common_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.enc2),str(item.last)])
	
	##write unique aps in wigle
	write_file.writerow([" "])
	write_file.writerow(["Wigle Unique",str(len(wigle_list))])
	write_file.writerow(["BSSID","SSID","Wigle-Encryption","Wigle-Channel"])
	for item in wigle_list:
		write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])
		
	##write unique aps in site
	write_file.writerow([" "])
	write_file.writerow(["Wigle Site Unique", str(len(site_list))])
	write_file.writerow(["BSSID","SSID","Site-Encryption","Last Update"])
	for item in site_list:
		write_file.writerow([str(item.bssid).upper(),str(item.ssid),str(item.enc),str(item.last)])
