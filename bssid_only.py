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
	if p.haslayer(Dot11) and p.type == 0 and p.subtype == 8 and p.addr2 not in unique_aps:
			unique_aps.append(p.addr2)
		##wrpcap('bsave_sniffed.pcaps',p,append=True)


##test = sniff(iface = 'wlan1', prn = callf)
# down wlan, monitor mode yung wlan, up wlan
sniff(prn = callf, offline="log-61.cap")

with open('log-61_beacon_macs.csv','wb') as csvfile:
	write_file = csv.writer(csvfile, delimiter = ',')
	write_file.writerow(["BSSID"])
	for item in unique_aps:
		write_file.writerow([str(item)])
	print "Analyzing finished"	
##wrpcap('bsave_sniffed2.pcap',test)
