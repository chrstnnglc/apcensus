#Compares the tricycle, ground truth, and WiGLE db readings (like a 3-circle venn diagram)
import csv
import operator


unique_trike = []
unique_gt = []
unique_wdb = []

common_trike_gt = []
common_trike_wdb = []
common_gt_wdb = []

common_all = []

class AP:
	def __init__(self, gps_time=None, time_capt=None, mac=None, ssid=None, sec=None, rssi=None, ch=None, manuf=None, ap_type=None,lat=None, lng=None, persistence=None, dates_seen=None):
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
                self.persistence = persistence
                self.dates_seen = dates_seen
                self.last_updt = ""     #will be equal to wigle db last updt if same ap/mac

class WDB:
        def __init__(self, last_updt=None, last_time=None, mac=None, ssid=None, sec=None, ch=None,lat=None, lng=None):
                self.last_updt = last_updt
                self.last_time = last_time
                self.mac = mac
                self.ssid = ssid
                self.security = sec
                self.channel = ch
                self.lat = lat
                self.lng = lng

#read tricycle readings first
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
                        persistence = line[11]
                        dates_seen = line[12]
                        new_ap = AP(gps_time,time_capt,mac,ssid,sec,rssi,ch,manuf,ap_type,lat,lng,persistence,dates_seen)
                        unique_trike.append(new_ap)
		i += 1

#read GT readings
i = 0			
with open('gtd_list.csv','rb') as csvfile:
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
                        new_ap = AP(gps_time,time_capt,mac,ssid,sec,rssi,ch,manuf,ap_type,lat,lng,"","")
                        unique_gt.append(new_ap)
                i += 1

#read WiGLE DB readings
i = 0			
with open('traversed_tve_wdb.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in reader:
                if i >= 1:   #ignore first line
                        last_updt = line[0]
                        last_time = line[1]
                        mac = line[2]
                        ssid = line[3]
                        sec = line[4]
                        ch = line[5]
                        lat = line[6]
                        lng = line[7]
                        new_ap = WDB(last_updt, last_time, mac, ssid, sec, ch, lat, lng)
                        unique_wdb.append(new_ap)
                i += 1
    

#get common to all
for ap1 in unique_trike:
    for ap2 in unique_gt:
        if ap1.mac == ap2.mac:
            for ap3 in unique_wdb:
                if ap1.mac == ap3.mac:
                    ap1.last_updt = ap3.last_updt
                    common_all.append(ap1)

#get common trike and gt
for ap1 in unique_trike:
    for ap2 in unique_gt:
        if ap1.mac == ap2.mac:
            common_trike_gt.append(ap1)

#get common trike and wdb
for ap1 in unique_trike:
    for ap3 in unique_wdb:
        if ap1.mac == ap3.mac:
            ap1.last_updt = ap3.last_updt
            common_trike_wdb.append(ap1)

#get common gt and wdb
for ap2 in unique_gt:
    for ap3 in unique_wdb:
        if ap2.mac == ap3.mac:
            ap2.last_updt = ap3.last_updt
            common_gt_wdb.append(ap2)

print "Unique to Trike: " + str(len(unique_trike))
print "Unique to GT: " + str(len(unique_gt))
print "Unique to WDB: " + str(len(unique_wdb))
print "Common to All: " + str(len(common_all))
print "Trike and GT: " + str(len(common_trike_gt))
print "Trike and WDB: " + str(len(common_trike_wdb))
print "GT and WDB: " + str(len(common_gt_wdb))

#Remove the duplicates of APs in common_all from all other list
for ap1 in common_all:
    for ap2 in common_trike_gt:
        if ap1.mac == ap2.mac:
            common_trike_gt.remove(ap2)
            break
    for ap2 in common_trike_wdb:
        if ap1.mac == ap2.mac:
            common_trike_wdb.remove(ap2)
            break
    for ap2 in common_gt_wdb:
        if ap1.mac == ap2.mac:
            common_gt_wdb.remove(ap2)
            break
    for ap2 in unique_trike:
        if ap1.mac == ap2.mac:
            unique_trike.remove(ap2)
            break
    for ap2 in unique_gt:
        if ap1.mac == ap2.mac:
            unique_gt.remove(ap2)
            break
    for ap2 in unique_wdb:
        if ap1.mac == ap2.mac:
            unique_wdb.remove(ap2)
            break

print "\nAfter Removing Common to All Duplicate... \n"
print "Unique to Trike: " + str(len(unique_trike))
print "Unique to GT: " + str(len(unique_gt))
print "Unique to WDB: " + str(len(unique_wdb))
print "Common to All: " + str(len(common_all))
print "Trike and GT: " + str(len(common_trike_gt))
print "Trike and WDB: " + str(len(common_trike_wdb))
print "GT and WDB: " + str(len(common_gt_wdb))

#Removing the duplicates of common_trike_gt from unique_trike and unique_gt
for ap1 in common_trike_gt:
    for ap2 in unique_trike:
        if ap1.mac == ap2.mac:
            unique_trike.remove(ap2)
            break
    for ap2 in unique_gt:
        if ap1.mac == ap2.mac:
            unique_gt.remove(ap2)
            break
        
#Removing duplicates of common_trike_wdb from unique_trike and unique_wdb
for ap1 in common_trike_wdb:
    for ap2 in unique_trike:
        if ap1.mac == ap2.mac:
            unique_trike.remove(ap2)
            break
    for ap2 in unique_wdb:
        if ap1.mac == ap2.mac:
            unique_wdb.remove(ap2)
            break

#Removing duplicates of common_gt_wdb from unique_gt and unique_wdb
for ap1 in common_gt_wdb:
    for ap2 in unique_gt:
        if ap1.mac == ap2.mac:
            unique_gt.remove(ap2)
            break
    for ap2 in unique_wdb:
        if ap1.mac == ap2.mac:
            unique_wdb.remove(ap2)
            break

print "\nAfter all Duplicates... \n"
print "Unique to Trike: " + str(len(unique_trike))
print "Unique to GT: " + str(len(unique_gt))
print "Unique to WDB: " + str(len(unique_wdb))
print "Common to All: " + str(len(common_all))
print "Trike and GT: " + str(len(common_trike_gt))
print "Trike and WDB: " + str(len(common_trike_wdb))
print "GT and WDB: " + str(len(common_gt_wdb))

#Printing Results. Make separate CSV files for each cross reference
with open('comp3-unique_trike.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude","Persistence","Dates Seen"])
    for item in unique_trike:
	write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng),str(item.persistence),str(item.dates_seen)])

with open('comp3-unique_gtd.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in unique_gt:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])
		
with open('comp3-unique_wdb.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["Last Updt","Last Time","MAC","SSID","Encryption","Channel","Latitude","Longitude"])
    for item in unique_wdb:
        write_file.writerow([str(item.last_updt),str(item.last_time),str(item.mac),str(item.ssid),str(item.security),str(item.channel),str(item.lat),str(item.lng)])
    
with open('comp3-trikexgt.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude","Persistence","Dates Seen"])
    for item in common_trike_gt:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng),str(item.persistence),str(item.dates_seen)])

with open('comp3-trikexwdb.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')    
    write_file.writerow(["GPS Time","LastUpdt(WDB)","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in common_trike_wdb:
        write_file.writerow([str(item.gps_time),str(item.last_updt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	

with open('comp3-gtxwdb.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',') 
    write_file.writerow(["GPS Time","LastUpdt(WDB)","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in common_gt_wdb:
        write_file.writerow([str(item.gps_time),str(item.last_updt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	
    
with open('comp3-cross_all.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["GPS Time","LastUpdt(WDB)","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude","Persistence","Dates Seen"])
    for item in common_all:
	write_file.writerow([str(item.gps_time),str(item.last_updt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng),str(item.persistence),str(item.dates_seen)])

