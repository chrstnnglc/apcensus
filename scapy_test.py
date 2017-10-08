import csv
import os
import pytz
from scapy.all import *

counter = 0
unique_aps = []
ap_list = []

'''
create AP object with attributes:
	mac
	ssid
	security
	channel
	bssid
	dmB
	average interval of beacon frames
'''

class AP:
	def __init__(self, bssid=None, ssid=None, sec=None, ch=None):
		self.bssid = bssid
		self.ssid = ssid
		self.security = sec
		self.channel = ch
		self.beacon_times = []
                self.signal_strengths = []
		self.avg_beacon_interval = 0
		self.avg_rssi = 0
	
	def append_time(self, beacon_t=None):
		self.beacon_times.append(beacon_t)

	def compute_avg(self):
		##count intervals of beacon frames
		beacon_intervals = []
		if len(self.beacon_times) == 1:	##if 1 beacon frame lang na receive
			self.avg_beacon_interval = -1
		else:	
			for i in range(len(self.beacon_times)):
				if i != 0:
					interval = self.beacon_times[i] - self.beacon_times[i-1]
					beacon_intervals.append(interval)

			##compute for the average beacon interval
			interval_count = len(beacon_intervals)
			summation = 0
			for i in beacon_intervals:
				summation += i
			avg = summation / interval_count
			self.avg_beacon_interval = avg
			
	def compute_avg_rssi(self):				
		rssi_count = len(self.signal_strengths)
		summation = 0
		for i in self.signal_strengths:
			summation += i
		avg = summation / rssi_count
		self.avg_rssi = avg	
				
def get_encryption(pkt):
	p = pkt[Dot11Elt]
	cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                      "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
	crypto = set()
	while isinstance(p, Dot11Elt):
		if p.ID == 0:
            		ssid = p.info
        	elif p.ID == 3:
            		channel = ord(p.info)
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
	if p.haslayer(Dot11) and p.type == 0 and p.subtype == 8:
		if p.addr2 not in unique_aps:
			unique_aps.append(p.addr2)
			bssid = p.addr2
			ssid = p.info
			channel = int(ord(p[Dot11Elt:3].info))
			enc = get_encryption(p)
			arrival_time = p.time
			rssi = -(256-ord(p.notdecoded[-2:-1]))
			
			new_ap = AP(bssid,ssid,enc,channel)
			new_ap.append_time(arrival_time)
			new_ap.append_rssi(rssi)
			ap_list.append(new_ap)
		else:									##append arrival time of packet to beacon_times
			arrival_time = p.time
			rssi = -(256-ord(p.notdecoded[-2:-1]))
			for item in ap_list:
				if item.bssid == p.addr2:
					item.append_time(arrival_time)
					item.append_rssi(rssi)
		##wrpcap('bsave_sniffed.pcaps',p,append=True)


##test = sniff(iface = 'wlan1', prn = callf)
# down wlan, monitor mode yung wlan, up wlan
sniff(prn = callf)

with open('newest_10.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	write_file.writerow(["BSSID","SSID","Encryption","Channel","Average Beacon Interval","Average Strength Signal"])
	for item in ap_list:
		item.compute_avg()
		print "MAC: %s, SSID: %s, Enc: %s, Channel: %d, Average Beacon Interval: %f, Average RSSI: %d" %(item.bssid,item.ssid,item.security,item.channel,item.avg_beacon_interval,item.avg_rssi)
		write_file.writerow([str(item.bssid), str(item.ssid), str(item.security), str(item.channel), str(item.avg_beacon_interval),str(item.avg_rssi)])
##wrpcap('bsave_sniffed2.pcap',test)
