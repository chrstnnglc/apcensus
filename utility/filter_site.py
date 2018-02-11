##THIS filters the list of aps in the Wigle site list that we have
##Remove all APs in the list that are not yet traversed in the map
import csv

unique_bssid = []
site_list = []
traversed_aps = []
filtered_list = []
newss = []
class AP:
	def __init__(self, ssid=None, bssid=None, lat=None, lng=None, enc=None, aptype=None, tid=None, ftime=None, ltime=None, lupdt=None):
		self.ssid = ssid
		self.bssid = bssid
		self.lat = lat
		self.lng = lng
		self.enc = enc
		self.aptype = aptype
		self.tid = tid
		self.ftime = ftime
		self.ltime = ltime
		self.lupdt = lupdt


with open('ap_list.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	i = 0
	for line in reader:
                if i != 0:		##ignore first line
                        ssid = line[0]
                        bssid = line[1].strip()
                        lat = line[2]
                        lng = line[3]
                        enc = line[4]
                        aptype = line[5]
                        tid = line[6]
                        ftime = line[7]
                        ltime = line[8]
			lupdt = line[9]
                        if bssid not in unique_bssid:
                                unique_bssid.append(bssid)
                                new_ap = AP(ssid,bssid,lat,lng,enc,aptype,tid,ftime,ltime,lupdt)
                                site_list.append(new_ap)
		i += 1

with open('filtered_wigle_db.txt','rb') as txt:
        i = 1
        for line in txt:
                if i % 2 == 1:
                        traversed_aps.append(line[1:].strip())
                i += 1


for mac in traversed_aps:
        for ap in site_list:
                if mac == ap.bssid:
                        filtered_list.append(ap)
                        break
                
with open('filtered_ap_list.csv','wb') as csvfile:
        write_file = csv.writer(csvfile, delimiter = ',')
        write_file.writerow(["SSID","Net ID","TriLat","TriLong","Encryption","Type","Trans ID","First Time","Last Time","Last Updt"])
        for ap in filtered_list:
                write_file.writerow([ap.ssid, ap.bssid, ap.lat, ap.lng, ap.enc, ap.aptype, ap.tid, ap.ftime, ap.ltime, ap.lupdt])
