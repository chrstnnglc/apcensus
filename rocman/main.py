from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint
from subprocess import call
import os
import hashlib

import settings
import constants
import script_argparser
import gps_thread
import trace_thread #apc edit
from utility_methods import *
from master import Mastery
from master import DistWinMastery
from slave import Slavery

if __name__ == "__main__":
	call(["clear"])

        parser = script_argparser.get_parser()
        args = parser.parse_args()
        if args.master:
                role = "master"
        elif args.slave:
                role = "slave"
                master_ip = args.slave # the argument passed to --slave contains the ip of master
        log_folder = args.log_dir
        wait_for_gps = args.wait_for_gps
        settings.server_ip = args.server
        settings.window_size = args.win_size
        settings.dist_thresh = args.dist_thresh
        settings.rssi_limit = args.rssi_limit
        settings.blacklist = args.blacklist
        settings.whitelist = args.whitelist
        settings.hash_macs = args.hash
        if settings.hash_macs:
                if settings.blacklist:
                        settings.blacklist = [hashlib.sha384(mac).hexdigest() for mac in settings.blacklist]
                if settings.whitelist:
                        settings.whitelist = [hashlib.sha384(mac).hexdigest() for mac in settings.whitelist]

        # check for monitors and stop them if there are any
	stop_monitors()

        # creates the folder which will contain all the logs if there isnt any yet
        if not os.path.exists(constants.logs_folder):
                os.makedirs(constants.logs_folder)

        if log_folder == None:
                # gets the list of logs, which follow the naming format "log-N"
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

	call(['airmon-ng', 'start', 'wlan1']) # will create a monitoring interface on mon0

        if role == "master":
                shark = trace_thread.SharkThread() #apc edit
                shark.start() #apc edit

                gps = gps_thread.GPSThread()
                gps.start()
                if wait_for_gps:
                        print("Waiting for the GPS to initialize...")
                        while gps.lat == 0 and gps.lon == 0:
                                time.sleep(1)
                if settings.window_size:
                        mastery = Mastery(log_folder, "mon0", gps)
                elif settings.dist_thresh:
                        mastery = DistWinMastery(log_folder, "mon0", gps)
                else: # should never happen
                        print("what do i base windowing on???")
                        exit()
                endpoint = TCP4ServerEndpoint(reactor, 8110)
                endpoint.listen(mastery)
        elif role == "slave":
                slavery = Slavery(log_folder, "mon0", gps = None)
                reactor.connectTCP(master_ip, 8110, slavery)
        else: # should never happen
                print("what am i? :thinking:")
	reactor.run()
	
        print('\nCapture stopped.')
        raw_input('Press ENTER to exit.\n')
else:
        print('This should only be run on main!')
