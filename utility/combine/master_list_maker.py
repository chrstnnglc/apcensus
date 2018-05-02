#Compare all csv files (ap_data.csv) one by one
#Creates a master list of all tricycle traces
import csv

unique_bssid = []
basis_list = []
insert_list = []
master_list = []
class AP:
	def __init__(self, gps_time=None, time_capt=None, mac=None, ssid=None, sec=None, rssi=None, ch=None, manuf=None, ap_type=None,lat=None, lng=None,):
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


#this will be our basis	list
i = 0
with open('master_list.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in reader:
        if i >= 1:   #ignore first line
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
            new_ap = AP(gps_time,time_capt,mac,ssid,sec,rssi,ch,manuf,ap_type,lat,lng)
            basis_list.append(new_ap)
        i += 1

#this will be the list that we will insert to master list
i = 0
with open('ap_data.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in reader:
        if i >= 1:   ##ignore first line
            
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
            new_ap = AP(gps_time,time_capt,mac,ssid,sec,rssi,ch,manuf,ap_type,lat,lng)
            insert_list.append(new_ap)
        i += 1

print "Basis: " + str(len(basis_list))
print "\nInsert: " + str(len(insert_list))

#compare the basis and insert lists
ap_index = []
ap2_index = []
for ap in basis_list:
    for ap2 in insert_list:
        if ap.mac == ap2.mac:
            #compare the rssi of common aps. retain the ap whose rssi is higher
            if int(ap.rssi) < int(ap2.rssi):
                ap_index.append(ap.mac)
            else:
                ap2_index.append(ap2.mac)

#remove the ap who has a duplicate and whose rssi is lower in its list
for i in range(len(ap_index)):
    for ap in basis_list:
        if ap_index[i] == ap.mac:
            basis_list.remove(ap)
            break
        
for i in range(len(ap2_index)):
    for ap2 in insert_list:
        if ap2_index[i] == ap2.mac:
            insert_list.remove(ap2)
            break

print "\nRemove from Basis: " + str(len(ap_index))
print "\nRemove from Insert: " + str(len(ap2_index))

print "\nBasis: " + str(len(basis_list))
print "\nInsert: " + str(len(insert_list))
    
#add remaning aps to master list            
master_list = basis_list + insert_list

print "\nMaster: " + str(len(master_list))

#make a csv file of master list
with open('master_list.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in master_list:
            write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	


#make a text file of master list
res_file = open("master_list.txt",'w')
for item in master_list:
	text = 	str(item.gps_time) +"|"+ str(item.time_capt) +"|"+ str(item.mac) +"|"+ str(item.ssid) +"|"+ str(item.security) +"|"+ str(item.rssi) +"|"+ str(item.channel) +"|"+ str(item.manuf) +"|"+ str(item.ap_type) +"|"+ str(item.lat) +"|"+ str(item.lng) + "\n"
	res_file.write(text)
res_file.close()
