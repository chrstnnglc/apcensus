import threading
from scapy.all import *
import constants
from utils import *

class MonitorThread(threading.Thread):
    def __init__(self, folder, gps = None):
        threading.Thread.__init__(self)
        self.pathname = folder
        self.gps = gps
        
    def run(self):
        beacons = []
        sniff(iface = constants.interface, prn = lambda p: phandle(p, beacons, self.pathname, self.gps), store = 0)

# Analyzes the channel of each packet
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
def phandle(p, beacons, log_folder, gps):
        if hasattr(p, "addr2") and p.addr2:                                 # If the packet actually has relevant mac information
	    mac = str(p.addr2)
	    # if the packet is a "beacon" or is a probe response to the request we sent
            if p.haslayer(Dot11Beacon) or (p.haslayer(Dot11ProbeResp) and p.addr1=="00:11:22:33:44:55"):     
                # added by apc, get time, mac, channel, rssi, and gps then write to bflog.txt
                    rssi = -(256-ord(p.notdecoded[-2:-1]))          
                    channel = get_p_ch(p)
                    ssid = ""
                    '''if hasattr(p, "info") and p.info:
                        ssid = p.info'''
                    #print "%s >> %s === %s / %s "%(timestamp(), mac, str(rssi), channel)
                    log_info = "%s | %s >> %s === %s / %s "%(get_time(gps.time), timestamp(), mac, str(rssi), channel)
                    log_info += "@%f,%f"%(gps.lat, gps.lon)
                    #log_info += " : %s"%(ssid)
                    log_write(log_folder + constants.bf_full_log_path, log_info + '\n')
                    #---------------------------------------------------------------------------
                        
                    if mac not in beacons:                          #registers new routers, hubs, etc
                        beacons.append(mac)
                        log_write(log_folder + constants.mac_log_path, mac + '\n')
                        #added by apc, aside from mac, add ssid in beacons.txt
                        '''log_info = "%s > %s" %(mac, ssid)
                        log_write(log_folder + constants.beacons_log_path, log_info + '\n')'''