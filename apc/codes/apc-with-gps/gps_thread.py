import gps
import threading
import constants
from utils import *   #added by apc

# A class which polls the GPS for the current location. The GPS typically updates every second.
class GPSThread(threading.Thread):
        def __init__(self, folder):     #added by apc from (self) to (self,folder)
                threading.Thread.__init__(self)
                self.daemon = True
                self.lat = 0
                self.lon = 0
                self.pathname = folder #added by apc
                
        def run(self):
                # watches the stream of data from the GPS port
                session = gps.gps("localhost", "2947")
                session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
                while True:
                    try:
                        report = session.next()
                        # if there is new data pertaining to location, then update the location data
                        if report.__dict__.has_key('lat') and report.__dict__.has_key('lon'):
                                self.lat = report.__dict__['lat']
                                self.lon = report.__dict__['lon']
                                # write every gps reading to a text file
                                log_info = "%s >> %f, %f" %(timestamp(), self.lat, self.lon)     #added by apc
                                log_write(self.pathname + constants.gps_readings, log_info + '\n') #added by apc
                                
                    except KeyError:
                        pass
