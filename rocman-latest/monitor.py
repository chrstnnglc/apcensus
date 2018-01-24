import threading
from scapy.all import *
import hashlib

import settings
import constants
from utility_methods import *

import sqlloggy as sqpy


# [NOTE] Although twisted does not particularly like conventional threading, this seemed like the only way since it would otherwise start blocking.
# Thread dedicated to the monitor-mode sniffer
class MonitorThread(threading.Thread):
	def __init__(self, factory, interface, gps = None):
		threading.Thread.__init__(self)
		self.factory = factory
		self.interface = interface
		self.gps = gps

	def run(self):
                # list of unique mac addresses
                umacs = []
                # list of "beacon" mac addresses, which pertains to those which act as routers or such, which we ignore
                # [NOTE] While this made sense for static deployment, we might want to remove this as this also filters out hotspots.
                beacons = []
                sqpy.startconn(self.factory.log_folder + "sql_log.db")
		sniff(iface = self.interface,
		      prn = lambda p: phandle(p, self.factory.log_folder, umacs, beacons, self.factory.window_umacs, self.gps),
		      store = 0,
		      stop_filter = lambda x: not self.factory.is_connected)
		
# added by apc, analyzes the packet and get channel information
def get_p_ch(pkt):
        p = pkt[Dot11Elt]
        cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                      "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
        channel = "X"   #default no channel or X
        
        while isinstance(p, Dot11Elt):
                if p.ID == 3:
                        if p.info:
                                channel = str(ord(p.info[0]))
                p = p.payload
        
        return channel
        
# Handles the packets coming in from sniffing
def phandle(p, log_folder, umacs, beacons, window_umacs, gps):
        if hasattr(p, "addr2") and p.addr2:                                 # If the packet actually has relevant mac information
		mac = str(p.addr2)
		if settings.hash_macs:
                        mac = hashlib.sha384(mac).hexdigest()
                if p.haslayer(Dot11Beacon):                             # if the packet is a "beacon"
                        # added by apc, get time, mac, channel, rssi, and gps then write to bflog.txt
                        rssi = -(256-ord(p.notdecoded[-2:-1]))          
                        channel = get_p_ch(p)
                        log_info = "%s >> %s === %s / %s "%(timestamp(), mac, str(rssi), channel)
                        if gps: # if gps data is being taken
                                log_info += "@%f,%f"%(gps.lat, gps.lon)
                        log_write(log_folder + constants.bf_full_log_path, log_info + '\n')
                        # ---------------------------------------------------------------------------
                        
                        if mac not in beacons:                          # registers new routers, hubs, etc
                                beacons.append(mac)
                                #added by apc, aside from mac, add ssid in beacons,txt
                                ssid = ""
                                if hasattr(p, "info") and p.info:
                                        ssid = p.info
                                log_info = "%s > %s" %(mac, ssid)
                                log_write(log_folder + constants.beacons_log_path, log_info + '\n')
                                #log_write(log_folder + constants.beacons_log_path, mac + '\n')
                if (mac not in beacons and                             # If the mac is registered as some sort of router or hub or whatever, ignore it
                (not settings.whitelist or mac in settings.whitelist) and   # If the whitelist exists, then only allow a mac if it is in that list
                (not settings.blacklist or mac not in settings.blacklist)): # If the blacklist exists, do not allow a mac if it is in that list
                        if mac not in umacs:
                                umacs.append(mac) # we add this to the list of all macs we've ever seen on this run
                                log_write(log_folder + constants.mac_log_path, mac + '\n')
                                if p.ID == 0:
                                        log_write(log_folder + constants.prmac_log_path, mac + '\n')

                        rssi = (256-ord(p.notdecoded[-2:-1]))
                        if rssi > 100: # while this technically shouldn't happen, it seems that it does. It seems to be when this field is not present.
                                rssi = "XX"

                        log_info = "%s >> %s --- %s"%(timestamp(), mac, str(rssi))
                        if gps: # if gps data is being taken
                                log_info += "@%f,%f"%(gps.lat, gps.lon)

                        if rssi < settings.rssi_limit: # passes a filter for signal strength, which we use to get a very rough estimate of distance (should be close enough) and remove "ambient packets"
                                if mac not in window_umacs:
                                        window_umacs.append(mac) # we add this to the list of all macs we've seen in this window
                        else:
                                log_info += " [EXCEEDED]"

                        #print(log_info)
                        #log info printing
                        if p.ID == 0:
                                log_write(log_folder + constants.prfull_log_path, log_info + '\n')
                        log_write(log_folder + constants.full_log_path, log_info + '\n')
                        sqpy.saveData(log_info)
