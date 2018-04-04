#by apc yes
import threading
import time
from subprocess import call
from scapy.all import *

class HopChThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
        #as we channel hop, we will also broadcast probe request to that channel   
        packet = RadioTap()/Dot11(type=0,subtype=4,addr1 = "ff:ff:ff:ff:ff:ff",addr2 = "00:11:22:33:44:55",addr3 = "ff:ff:ff:ff:ff:ff")/Dot11Elt(ID="SSID",info="")
        while True:
            for channel in range(1,14):
                call(['sudo', 'iwconfig', 'wlan1', 'channel', str(channel)])
                print "wlan1 Current Channel: " + str(channel)
                sendp(packet,iface="wlan1")
                time.sleep(1)