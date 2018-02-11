import csv

res_file = open("teachersvill/parsed_wiglesite.txt","w")

unique_bssid = []
wigle_list = []

class AP:
	def __init__(self, ssid=None,bssid=None, coord=None, rssi=None, channel=None):
                self.ssid = ssid
		self.bssid = bssid
		self.coord = coord
		self.rssi = rssi
		self.channel = channel

with open('teachersvill/ap_list.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	i = 0
	for row in reader:
		if i > 0:	##ignore first line, what if ignore din lastupd < 2017????
			row = ','.join(row)
			line = row.split(',')

			ssid = line[0]
			ssid = ssid.replace("'", '')
			bssid = line[1]
			channel = "none"
			rssi = "none"
			lat = line[2]
			lng = line[3]
			coord = "%s,%s" %(lat,lng)
			if bssid not in unique_bssid:
				unique_bssid.append(bssid)
				new_ap = AP(ssid,bssid,coord,rssi,channel)
				wigle_list.append(new_ap)
		i += 1
		
for item in wigle_list:
    text = str(item.ssid) + " | " + str(item.bssid) + " | " + str(item.coord) + " | " + str(item.rssi) + " | " + str(item.channel) + "\n"
    res_file.write(text)

res_file.close()
