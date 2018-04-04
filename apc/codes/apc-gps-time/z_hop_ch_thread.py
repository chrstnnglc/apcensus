#by apc yes
import threading
import time
from subprocess import call
from scapy.all import *

class HopChThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
        ch_list = [1, 6, 11]
        #as we channel hop, we will also broadcast probe request to that channel   
        packet = RadioTap()/Dot11(type=0,subtype=4,addr1 = "ff:ff:ff:ff:ff:ff",addr2 = "00:11:22:33:44:55",addr3 = "ff:ff:ff:ff:ff:ff")/Dot11Elt(ID="SSID",info="")
        while True:
            for channel in ch_list:
                call(['sudo', 'iwconfig', 'wlan2', 'channel', str(channel)])
                print "wlan2 Current Channel: " + str(channel)
                sendp(packet,iface="wlan2")
                time.sleep(1)