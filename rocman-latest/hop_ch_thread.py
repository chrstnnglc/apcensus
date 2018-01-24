#by apc yes

import threading
import time
from subprocess import call

class HopChThread (threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
        while True:
            for channel in range(1,14):
                call(['sudo', 'iwconfig', 'wlan1', 'channel', str(channel)])
                print "Current Channel: " + str(channel)
                time.sleep(1)
        
