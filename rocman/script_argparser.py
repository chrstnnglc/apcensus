import argparse
import re
import os

import settings
from utility_methods import *

def valid_ip(string):
        if string == None:
                return string
        else:
                if is_ip(string):
                        return string
                else:
                        raise argparse.ArgumentTypeError("IP given (%s) is invalid"%(string))

def positive_float(num):
        try:
                num = float(num)
        except ValueError:
                raise argparse.ArgumentTypeError("%s is not a number!"%(num))
        if num > 0:
                return num
        else:
                raise argparse.ArgumentTypeError("%s should be positive!"%(num))

def valid_rssi(rssi):
        try:
                rssi = int(rssi)
        except ValueError:
                raise argparse.ArgumentTypeError("RSSI given (%s) is invalid"%(rssi))
        if 0 <= rssi and rssi <= 100:
                return rssi
        else:
                raise argparse.ArgumentTypeError("RSSI given (%s) is not within the range 0-100"%(rssi))

def valid_existing_path(path):
        if os.path.exists(path):
                return path
        else:
                raise argparse.ArgumentTypeError("%s does not exist"%(path))

def valid_new_path(path):
        if path == None:
                return path
        else:
                if type(path) == str: #tentative, should check if valid path string later
                        if os.path.exists(path):
                                raise argparse.ArgumentTypeError("%s already exists"%(path))
                        else:
                                if path[-1] != "/":
                                        path += "/"
                                return path
                else:
                        raise argparse.ArgumentTypeError("%s is not a valid path"%(path))
        
def valid_mac(mac):
        if is_mac(mac):
                return mac
        else:
                raise argparse.ArgumentTypeError("%s is not a mac address"%(mac))

def valid_macfile(mac_file):
        if os.path.exists(mac_file):
                mac_list = read_list(mac_file)
                for mac in mac_list:
                        if not is_mac(mac):
                                raise argparse.ArgumentTypeError("%s is not a mac address"%(mac))
                return mac_list
        else:
                raise argparse.ArgumentTypeError("%s does not exist"%(mac_file))

def get_parser(role_check = True):
        parser = argparse.ArgumentParser(description = "no description yet")
        if role_check:
                role_group = parser.add_mutually_exclusive_group(required = True)
                role_group.add_argument("-s", "--slave", action = "store", type = valid_ip, metavar = "MASTER_IP",
                                        help = "use this argument to take the role of a slave, connecting to the master at MASTER_IP")
                role_group.add_argument("-m", "--master", action = "store_true",
                                help = "use this argument to take the role of master")
        window_group = parser.add_mutually_exclusive_group(required = True)
        window_group.add_argument("-t", "--win-size", "--window-size", action = "store", nargs = "?", type = positive_float, const = 10.0, default = None,
                            help = "will use time to start a new window. a value for the interval in seconds can be given. if no value is provided, it will default to 10 seconds")
        window_group.add_argument("-x", "--dist-thresh", "--distance-threshold", action = "store", nargs = "?", type = positive_float, const = 9e-9, default = None,
                            help = "will use distance to start a new window. a value for the interval can be given. if no value is provided, it will default to 9e-09")
        parser.add_argument("-c", "--server", "--connect-to-server", nargs = "?", type = valid_ip, const = "202.92.132.190", default = None,
                            help = "if given, connects to server at the given IP (default server is 202.92.132.190)")
        gps_group = parser.add_mutually_exclusive_group()
        gps_group.add_argument("-i", "--ignore-gps", action = "store_true",
                            help = "if given, will ignore the absence of a gps and assume mastery anyway.")
        gps_group.add_argument("-w", "--wait", "--wait-for-gps", dest = "wait_for_gps", action = "store_true",
                            help = "if given, will wait for the gps to get a reading before beginning capture.")
        parser.add_argument("--hash", "--hash-macs", action = "store_true",
                            help = "if given, the script will hash all macs before processing")
        parser.add_argument("-r", "--rssi-limit", "--limit", dest = "rssi_limit", action = "store", type = valid_rssi, default = 100,
                            help = "imposes a limit on the rssi (signal strength) from 0-100, with 0 being the best and 100 being the worst signal. (default value is 100)")
        parser.add_argument("-d", "--log-dir", action = "store", type = valid_new_path, default = None,
                            help = "chooses the directory to write this log to")
        blacklist_group = parser.add_mutually_exclusive_group()
        blacklist_group.add_argument("--blacklist", action = "store", nargs = "+", type = valid_mac,
                            help = "prevents all mac addresses specified in the arguments from being processed by the script")
        blacklist_group.add_argument("--blacklist-file", dest = "blacklist", metavar = "BLACKLIST_FILE", action = "store", type = valid_macfile,
                            help = "prevents all mac addresses specified in the file (separated by newlines) from being processed by the script")
        whitelist_group = parser.add_mutually_exclusive_group()
        whitelist_group.add_argument("--whitelist", action = "store", nargs = "+", type = valid_mac,
                            help = "allows only the mac addresses specified in the arguments to be processed by the script")
        whitelist_group.add_argument("--whitelist-file", dest = "whitelist", metavar = "WHITELIST_FILE", action = "store", type = valid_macfile,
                            help = "allows only the mac addresses specified in the file (separated by newlines) to be processed by the script")
        return parser

# for testing
if __name__ == "__main__":
        parser = get_parser()
        args = parser.parse_args()
        print("#"*20)
        for (key, arg) in vars(args).items():
                print("%s: %s"%(key, arg))
        print("-"*20)
        if args.master:
                print("i am the pokemon master")
                role = "master"
        elif args.slave:
                print("i am a slave with master at %s"%(args.slave))
                role = "slave"
                master_ip = args.slave
        if args.server:
                print("i will connect to the server at %s"%(args.server))
        settings.server_ip = args.server
        if args.ignore_gps:
                print("i will ignore the absence of the gps")
        settings.gps_not_needed = args.ignore_gps
        if args.wait_for_gps and not args.ignore_gps:
                print("i will wait for the gps to start first")
        settings.wait_for_gps = args.wait_for_gps and not args.ignore_gps
        if args.win_size:
                print("i will window based on time with a window size of %g seconds"%(args.win_size))
        elif args.dist_thresh:
                print("i will window based on distance with a threshold of %g"%(args.dist_thresh))
        settings.window_size = args.win_size
        settings.dist_thresh = args.dist_thresh
        if args.hash:
                print("i will hash macs before processing")
        settings.hash_macs = args.hash
        if args.rssi_limit < 100:
                print("i will limit the rssi value to %d"%(args.rssi_limit))
        else:
                print("i will not limit the rssi value")
        settings.rssi_limit = args.rssi_limit
        if args.log_dir:
                print("i will write this log to %s instead"%(args.log_dir))
        log_folder = args.log_dir
        if args.blacklist:
                print("the following mac addresses will be ignored:")
                for mac in args.blacklist:
                        print("\t" + mac)
        settings.blacklist = args.blacklist
        if args.whitelist:
                print("all mac addresses not included here will be ignored:")
                for mac in args.whitelist:
                        print("\t" + mac)
        settings.whitelist = args.whitelist

        #non-printing:
        if False: #disabled
                parser = get_parser()
                args = parser.parse_args()
                if args.master:
                        role = "master"
                elif args.slave:
                        role = "slave"
                        master_ip = args.slave
                log_folder = args.log_dir
                settings.server_ip = args.server
                settings.gps_not_needed = args.ignore_gps
                settings.wait_for_gps = args.wait_for_gps
                settings.window_size = args.win_size
                settings.dist_thresh = args.dist_thresh
                settings.hash_macs = args.hash
                settings.rssi_limit = args.rssi_limit
                settings.blacklist = args.blacklist
                settings.whitelist = args.whitelist
                
