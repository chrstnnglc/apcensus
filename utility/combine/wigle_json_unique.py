#Combine Wigle DB data first using wigle_json_combiner.py
#Use this to remove duplicate APs

import csv
import datetime

class AP:
    def __init__(self, last_updt=None, last_time=None, mac=None, ssid=None, sec=None, ch=None,lat=None, lng=None):
        self.last_updt = last_updt
        self.last_time = last_time
	self.mac = mac
	self.ssid = ssid
	self.security = sec
	self.channel = ch
	self.lat = lat
	self.lng = lng

def time_convert(time_in):
        formatto = "%Y-%m-%d %H:%M:%S"
        formatfrom = "%Y-%m-%d, %I:%M:%S %p"
        time_out = datetime.datetime.strptime(time_in,formatfrom)
        time_out = time_out.strftime(formatto)
        return time_out

#Initialize APs we need to filter out
ap_list = []
unique_macs = []
i=0
with open('ap_list.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for line in reader:
        if i >= 1:   #ignore first line
            last_updt = time_convert(line[10])
            last_time = time_convert(line[9])
            mac = line[1].lower()
            ssid = line[0]
            sec = line[4]
            ch = line[5]
            lat = line[2]
            lng = line[3]
            if mac not in unique_macs:
                unique_macs.append(mac)
                new_ap = AP(last_updt, last_time, mac, ssid, sec, ch, lat, lng)
                ap_list.append(new_ap)
            else:
                for item in ap_list:
                    if item.mac == mac:
                        if item.last_updt < last_updt:
                            item.last_updt = last_updt
                            item.last_time = last_time
                            item.lat = lat
                            item.lng = lng
        i+=1

#create a csv file of unique wigle db list
with open('payatas_wdb.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["Last Updt","Last Time","MAC","SSID","Encryption","Channel","Latitude","Longitude"])
    for item in ap_list:
        write_file.writerow([str(item.last_updt),str(item.last_time),str(item.mac),str(item.ssid),str(item.security),str(item.channel),str(item.lat),str(item.lng)])
    
#create a txt file of unique wigle db list
res_file = open("payatas_wdb.txt",'w')
for item in ap_list:
    text = str(item.last_updt) +"|"+ str(item.last_time) +"|"+ str(item.mac) +"|"+ str(item.ssid) +"|"+ str(item.security) +"|"+ str(item.channel) +"|"+ str(item.lat) +"|"+ str(item.lng) +"\n"
    res_file.write(text)  
res_file.close()
