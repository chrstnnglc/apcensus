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
		#self.beacon_times = []
		#self.signal_strengths = []
		self.packets_captured = 0
		self.sum_interval = 0
		self.sum_rssi = 0
		self.avg_beacon_interval = 0
		self.avg_rssi = 0

		self.prev_time = 0
		self.new_time = 0

	def add_num_packets(self):
		self.packets_captured += 1

	def compute_avg(self):
		if self.sum_interval == 0:
			self.avg_beacon_interval = -1
		else:
			self.avg_beacon_interval = self.sum_interval / self.packets_captured
			
	def compute_avg_rssi(self):				
		self.avg_rssi = self.sum_rssi / self.packets_captured
				
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
			bssid = p.addr2
			ssid = p.info
			channel = ord(p[Dot11Elt:3].info[0])
			enc = get_encryption(p)
			arrival_time = p.time
			rssi = -(256-ord(p.notdecoded[-2:-1]))
			
			new_ap = AP(bssid,ssid,enc,channel)
			new_ap.prev_time = arrival_time
			new_ap.sum_rssi += rssi
			new_ap.add_num_packets()
			ap_list.append(new_ap)
		else:
			arrival_time = p.time
			rssi = -(256-ord(p.notdecoded[-2:-1]))
			for item in ap_list:
				if item.bssid == p.addr2:
					item.add_num_packets()
					item.sum_rssi += rssi       		                ##add rssi to summation of rssi
					item.new_time = arrival_time  		                ##compute for interval first then add interval to summation of intervals
					item.sum_interval += item.new_time - item.prev_time
					item.prev_time = item.new_time
		##wrpcap('bsave_sniffed.pcaps',p,append=True)


##test = sniff(iface = 'wlan1', prn = callf)
# down wlan, monitor mode yung wlan, up wlan
sniff(prn = callf, offline="log-76.pcap")

with open('log-76.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	write_file.writerow(["BSSID","SSID","Encryption","Channel","Average Beacon Interval","Average Strength Signal","Number of Packets","Interval Summation","RSSI Summation"])
	for item in ap_list:
		item.compute_avg()
		item.compute_avg_rssi()
		print "MAC: %s, SSID: %s, Enc: %s, Channel: %s, Average Beacon Interval: %f, Average RSSI: %d, No. of Packets: %d" %(item.bssid,item.ssid,item.security,item.channel,item.avg_beacon_interval,item.avg_rssi,item.packets_captured)
		write_file.writerow([str(item.bssid), str(item.ssid), str(item.security), str(item.channel), str(item.avg_beacon_interval),str(item.avg_rssi),str(item.packets_captured),str(item.sum_interval),str(item.sum_rssi)])
	print "Analyzing finished"	
##wrpcap('bsave_sniffed2.pcap',test)