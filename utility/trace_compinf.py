#Combine info from bflog.txt and trace.pcap then make a csv file
import csv
import os
import pytz
from scapy.all import *
from oui_dict import *

counter = 0
unique_aps = []
ap_list = []

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


def get_encryption(pkt):
	p = pkt[Dot11Elt]
	cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                      "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
	crypto = set()
	while isinstance(p, Dot11Elt):
		if p.ID == 0:
            		ssid = p.info
        	elif p.ID == 48:
            		crypto.add("WPA2")
        	elif p.ID == 221 and p.info.startswith('\x00P\xf2\x01\x01\x00'):
            		crypto.add("WPA")
        	p = p.payload

	if not crypto:
		if 'privacy' in cap:
			crypto.add("WEP")
		else:
			crypto.add("OPN")

	encryption = '/'.join(crypto)
	return encryption

def callf(p):
	global counter
	counter += 1
	print "Analyzing packet no. %d" %(counter)
	if p.haslayer(Dot11) and p.type == 0 and p.subtype == 8:
		if p.addr2 not in unique_aps:
			unique_aps.append(p.addr2)
			
			mac = p.addr2
			ssid = p.info
			enc = get_encryption(p)
			channel = ord(p[Dot11Elt:3].info[0])
			manuf = oui_lookup(mac[0:8])
			rssi = -(256-ord(p.notdecoded[-2:-1]))
			
			new_ap = AP("none","none",mac,ssid,enc,rssi,channel,manuf,"none","none","none")
			ap_list.append(new_ap)
		else:
                        rssi = -(256-ord(p.notdecoded[-2:-1]))
                        for item in ap_list:
                                if item.bssid == p.addr2:
                                        if item.rssi < rssi:
                                                item.rssi = rssi

#----------------------------------------------------------------------------------------------------------------------------------
sniff(prn = callf, offline="trace.pcap")

unique_aps = []
ap_list2 = []
bf_file = open("bflog.txt","r")
#read the bflog.txt file (we will get the time, lat, and lng)
for line in bf_file:
    parsed = line.split()
    for i in range(0,len(parsed)):
        parsed[i] = parsed[i].strip()
    
    gps_time = parsed[0] + parsed[1]
    time_capt = parsed[3] + parsed[4]
    mac = parsed[6]
    rssi = parsed[8]
    loc = parsed[11]
    loc = loc[1:]
    loc = loc.split(",")
    lat = loc[0]
    lng = loc[1]
    if mac not in unique_aps:
        unique_aps.append(mac)
        new_ap = AP(gps_time,time_capt,mac,"none","none",rssi,"none","none","none",lat,lng)
	ap_list2.append(new_ap)
    else:
        for item in ap_list2:
            if item.mac == mac:
                if int(item.rssi) < int(rssi):
                    item.gps_time = gps_time
                    item.time_capt = time_capt
                    item.rssi = rssi
		    item.lat = lat
		    item.lng = lng

print len(ap_list)
print len(ap_list2)
#we now combine information on both lists to complete our data for the ap
for ap in ap_list:
    for ap2 in ap_list2:
        if ap.mac == ap2.mac:
            ap.gps_time = ap2.gps_time
            ap.time_capt = ap2.time_capt
            ap.lat = ap2.lat
            ap.lng = ap2.lng

#if coordinates are 0, we remove that ap in our list
#..........
#make csv file
'''with open('trace.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	write_file.writerow(["GPS Time","Time,""MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
	for item in ap_list:
        
	print "Analyzing finished"
'''
