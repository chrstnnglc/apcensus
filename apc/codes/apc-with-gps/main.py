import os
import constants
from utils import *
from subprocess import call

import monitor
import hop_ch_thread #apc edit
import trace_thread #apc edit
import gps_thread

if __name__ == "__main__":
    # set the interface to monitor mode
    call(['sudo', 'ifconfig', 'wlan1', 'down'])
    call(['sudo','iwconfig','wlan1','mode','monitor'])
    call(['sudo', 'ifconfig', 'wlan1', 'up'])
    
    # start the gps
    call(['sudo', 'killall', 'gpsd'])
    call(['sudo', 'gpsd', '/dev/ttyUSB0', '-F', '/var/run/gpsd.sock'])
    
    # creates the folder which will contain all the logs if there isnt any yet
    if not os.path.exists(constants.logs_folder):
        os.makedirs(constants.logs_folder)
        
    logs = [log for log in os.listdir(constants.logs_folder) if is_log(log)]

    if logs: # if there are any logs
        log_numbers = [get_log_number(log) for log in logs] # get the numerical values of all such logs
        log_number = max(log_numbers) + 1 # sets the new log number to be after the last log
    else:
        log_number = 1 # defaults to 1
    log_folder = constants.logs_folder + 'log-' + str(log_number) + '/'
        
    # creates the folder for the new log, assuming there is none (there shouldn't be any)
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)
    
    gps = gps_thread.GPSThread(log_folder) # apc edit, addded log_folder param
    gps.start()
    hop = hop_ch_thread.HopChThread() # apc edit
    hop.start() # apc edit
    sniffing = monitor.MonitorThread(log_folder, gps)
    sniffing.start()
    shark = trace_thread.TraceThread(log_folder) # apc edit
    shark.start() # apc edit 