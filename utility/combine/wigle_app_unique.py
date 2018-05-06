#Reads wigle app csv files and make a list of unique APs from them
import csv
unique_macs = []
wapp_list = []

class WA:
        def __init__(self, time_capt=None, mac=None, ssid=None, sec=None, rssi=None, ch=None,lat=None, lng=None):
                self.time_capt = time_capt
                self.mac = mac
                self.ssid = ssid
                self.sec = sec
                self.rssi = rssi
                self.ch = ch
                self.lat = lat
                self.lng = lng


#read Wigle App reading
i = 0	
with open('gtn_wigle.csv','rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in reader:
            if i > 1:   #ignore first 2 lines
                mac = line[0]
                ssid = line[1]
                sec = line[2]
                time_capt = line[3]
                ch = line[4]
                rssi = line[5]
                lat = line[6]
                lng = line[7]
                if mac not in unique_macs:
                    unique_macs.append(mac)
                    new_ap = WA(time_capt,mac,ssid,sec,rssi,ch,lat,lng)
                    wapp_list.append(new_ap)
                else:
                    for item in wapp_list:
                        if item.mac == mac:
                            if int(item.rssi) < int(rssi):
                                item.time_capt = time_capt
                                item.rssi = rssi
                                item.lat = lat
                                item.lng = lng
            i += 1

#create a csv file containing unique APs
with open('gtn_wigle_unique.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["First Seen","MAC","SSID","Encryption","RSSI","Channel","Latitude","Longitude"])
    for item in wapp_list:
        write_file.writerow([str(item.time_capt),str(item.mac),str(item.ssid),str(item.sec),str(item.rssi),str(item.ch),str(item.lat),str(item.lng)])
