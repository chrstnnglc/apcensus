#by apc yes

import threading
from subprocess import call

class TraceThread (threading.Thread):
   def __init__(self, folder):
      threading.Thread.__init__(self)
      self.pathname = folder
   def run(self):
      call (['sudo','ifconfig','wlan1','down'])
      call (['sudo','iwconfig','wlan1','mode','monitor'])
      call (['sudo','ifconfig','wlan1','up'])
      call(['sudo', 'tcpdump', '-i', 'wlan1', '-e', '-w', self.pathname + 'trace.pcap', 'type', 'mgt'])
      '''call(['sudo','airmon-ng','start','wlan1'])
      call(['sudo','airmon-ng','stop','wlan1'])
      call(['sudo', 'airodump-ng','wlan1','-w', self.pathname + 'trace', '-o','pcap'])'''
