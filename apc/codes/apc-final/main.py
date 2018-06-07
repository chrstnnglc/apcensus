import os
import constants
from utils import *
from subprocess import call

import monitor
import hop_ch_thread 
import trace_thread 
import gps_thread

#uncomment this block if you want to use 1-6-11 channel hopping scheme
'''
import z_monitor          
import z_hop_ch_thread    
import z_trace_thread     
'''

if __name__ == "__main__":
    # set the interface to monitor mode
    call(['sudo', 'ifconfig', constants.interface, 'down'])
    call(['sudo','iwconfig', constants.interface,'mode','monitor'])
    call(['sudo', 'ifconfig', constants.interface, 'up'])

    #uncomment this block if you want to use 1-6-11 channel hopping scheme
    '''
    call(['sudo', 'ifconfig', constants.z_interface, 'down'])            
    call(['sudo','iwconfig', constants.z_interface,'mode','monitor'])     
    call(['sudo', 'ifconfig', constants.z_interface, 'up'])
    '''
    
    # start the gps
    call(['sudo', 'systemctl', 'enable', 'gpsd.socket'])
    call(['sudo', 'systemctl', 'start', 'gpsd.socket'])
    
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
    
    gps = gps_thread.GPSThread(log_folder)
    gps.start()
    hop = hop_ch_thread.HopChThread()
    hop.start()
    sniffing = monitor.MonitorThread(log_folder, gps)
    sniffing.start()
    shark = trace_thread.TraceThread(log_folder)
    shark.start()

    #uncomment this block if you want to use 1-6-11 channel hopping scheme
    '''
    z_hop = z_hop_ch_thread.HopChThread()                  
    z_hop.start()                                          
    z_sniffing = z_monitor.MonitorThread(log_folder, gps)  
    z_sniffing.start()                                     
    z_shark = z_trace_thread.TraceThread(log_folder)       
    z_shark.start()                                        
    '''
    
