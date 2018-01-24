import threading
from scapy.all import *
import constants
from utils import *

class MonitorThread(threading.Thread):
    def __init__(self, folder):
        threading.Thread.__init__(self)
        self.pathname = folder
        
    def run(self):
        beacons = []
        sniff(iface = constants.interface, prn = lambda p: phandle(p, beacons, self.pathname), store = 0)
        
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
def phandle(p, beacons, log_folder):
        if hasattr(p, "addr2") and p.addr2:                                 # If the packet actually has relevant mac information
	    mac = str(p.addr2)
            if p.haslayer(Dot11Beacon):                             # if the packet is a "beacon"
                # added by apc, get time, mac, channel, rssi, and gps then write to bflog.txt
                    rssi = -(256-ord(p.notdecoded[-2:-1]))          
                    channel = get_p_ch(p)
                    #print "%s >> %s === %s / %s "%(timestamp(), mac, str(rssi), channel)
                    
                    log_info = "%s >> %s === %s / %s "%(timestamp(), mac, str(rssi), channel)
                    #log_info += "@%f,%f"%(gps.lat, gps.lon)
                    log_write(log_folder + constants.bf_full_log_path, log_info + '\n')
                    #---------------------------------------------------------------------------
                        
                    if mac not in beacons:                          #registers new routers, hubs, etc
                        beacons.append(mac)
                        #added by apc, aside from mac, add ssid in beacons,txt
                        ssid = ""
                        if hasattr(p, "info") and p.info:
                            ssid = p.info
                            log_info = "%s > %s" %(mac, ssid)
                            log_write(log_folder + constants.beacons_log_path, log_info + '\n')