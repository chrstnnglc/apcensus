import csv

res_file = open("parsed_wigle.txt","w")

unique_bssid = []
wigle_list = []

class AP:
	def __init__(self, bssid=None, coord=None, rssi=None, channel=None):
		self.bssid = bssid
		self.coord = coord
		self.rssi = rssi
		self.channel = channel

with open('wigle-76.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='|')
	i = 0
	for row in reader:
		if i > 1:	##ignore first 2 lines
			row = ','.join(row)
			line = row.split(',')
			
			bssid = line[0]
			channel = line[4]
			rssi = line[5]
			lat = line[6]
			lng = line[7]
			beacon_type = line[10]
			coord = "%s,%s" %(lat,lng)
			
			if bssid not in unique_bssid and beacon_type == "WIFI":     #we remove the GSM types (Globe idk)
				unique_bssid.append(bssid)
				new_ap = AP(bssid,coord,rssi,channel)
				wigle_list.append(new_ap)
			else:
				for item in wigle_list:
					if bssid == item.bssid:
                                                if int(item.rssi) < int(rssi):
                                                        item.rssi = rssi
                                                        item.coord = coord
		i += 1
for item in wigle_list:
    text = str(item.bssid) + " = " + str(item.coord) + " = " + str(item.rssi) + " = " + str(item.channel) + "\n"
    res_file.write(text)

res_file.close()
    
