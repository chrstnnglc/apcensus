#this generates a pcap file using tcpdump

import threading
import constants
from subprocess import call

class TraceThread (threading.Thread):
   def __init__(self, folder):
      threading.Thread.__init__(self)
      self.pathname = folder
   def run(self):
      # we cut the pcap files into 15 MB 
      call(['sudo', 'tcpdump', '-i', constants.interface, '-e', '-C', '15', '-w', self.pathname + 'trace.pcap', 'type', 'mgt'])
