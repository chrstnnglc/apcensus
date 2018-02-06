##THIS PARSES bflogs.txt files in ROCMAN.
file = open("teachersvill/z_bflog.txt","r")
res_file = open("teachersvill/parsed_z_bflog.txt","w")

unique_aps = []
ap_list = []

class AP:
	def __init__(self, bssid=None, coord=None, rssi=None, channel=None):
		self.bssid = bssid
		self.coord = coord
		self.rssi = rssi
		self.channel = channel

for line in file:
        parsed = line.split()
        bssid = parsed[3]
        rssi = parsed[5]
        channel = parsed[7]
        coord = parsed[8]
        coord = coord[1:]               #remove the @ symbol

        ##only consider those with gps readings
        if coord != "0.000000,0.000000":
                if bssid not in unique_aps:
                        new_ap = AP(bssid,coord,rssi,channel)
			unique_aps.append(bssid)
			ap_list.append(new_ap)
		else:
			for item in ap_list:
				##check if its rssi in this reading is smaller than its current record in ap_list then replace its current rssi and coordinate
				if item.bssid == bssid:
					if int(item.rssi) < int(rssi):
						item.rssi = rssi
						item.coord = coord

##print results
for item in ap_list:
	text = str(item.bssid) + " = " + str(item.coord) + " = " + str(item.rssi) + " = " + str(item.channel) + "\n"
	res_file.write(text)

file.close()
res_file.close()
