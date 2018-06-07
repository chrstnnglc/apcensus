#This generates a pcap file using tcpdump for 1-6-11 channel hopping scheme
import threading
import constants
from subprocess import call

class TraceThread (threading.Thread):
   def __init__(self, folder):
      threading.Thread.__init__(self)
      self.pathname = folder
   def run(self):
      # we cut the pcap files into 15 MB 
      call(['sudo', 'tcpdump', '-i', constants.z_interface, '-e', '-C', '15', '-w', self.pathname + 'z_trace.pcap', 'type', 'mgt'])
   

