import datetime
import re
from subprocess import call

def is_ip(ip):
        # solution using casting (runs approx. 37% slower than condensed regex)
        ##ip_parts = string.split(".")
        ##try:
        ##        ip_parts = [int(part) for part in ip_parts]
        ##except ValueError:
        ##        raise argparse.ArgumentTypeError("IP given (%s) is invalid"%(string))
        ##return all([(0 <= part and part <= 255) for part in ip_parts]) and len(ip_parts) == 4:
        
        # solution via regex (runs approx. 54% slower than condensed regex)
        ##_0to199    = "[0-1]?[0-9]?[0-9]"
        ##_200to249  = "2[0-4][0-9]"
        ##_250to255  = "25[0-5]"
        ##_0to255    = "(%s|%s|%s)"%(_0to199, _200to249, _250to255)
        ##ip_address = "%s\.%s\.%s\.%s$"%(_0to255, _0to255, _0to255, _0to255)
        ##return re.match(ip_address, string):
        
        # condensed regex solution (takes approx 0.35 sec to finish 256^2 times on my machine) (run on 0.0.0.0 to 0.0.255.255)
        # plugging the ip_address value into re.match directly has no significant improvement
        # MICRO-OPTIMIZATION BOIIIIIIIIIIIIIIIII
        ip_address = "([0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.([0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.([0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])\.([0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])$"
        return re.match(ip_address, ip)

# determines whether the string conforms to the "log-N" format
def is_log(log):
        return re.match("log-[0-9]+$", log)

# returns only the number of the log (removes the initial "log-" of "log-N" and returns N)
# assumes the form has been validated previously
def get_log_number(log):
        return int(log[4:])

# determines whether the string data is valid
def is_valid(data):
        return is_maclist(data) or is_hashlist(data)

# determines whether the string data is a mac address
def is_mac(data):
        ##hex_digit = "[0-9A-Fa-f]"
        ##mac_address = "(" + hex_digit + "{2}(:" + hex_digit + "{2}){5})"
        ##return bool(re.match(mac_address + "$", data))
        return bool(re.match("([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})$", data))

# determines whether the string data is a hash
def is_hash(data):
        ##hex_digit = "[0-9A-Fa-f]"
        ##hashed_mac = "(" + hex_digit + "{96})"
        ##return bool(re.match(hashed_mac + "$", data))
        return bool(re.match("([0-9A-Fa-f]{96})$", data))

def is_valid_list(l):
        return is_maclist(l) or is_hashlist(l)

def is_maclist(macs):
        ##hex_digit = "[0-9A-Fa-f]"
        ##mac_address = "(" + hex_digit + "{2}(:" + hex_digit + "{2}){5})"
        ##mac_list = mac_address + "?(;" + mac_address + ")*$"
        ##return bool(re.match(mac_list, macs))
        return bool(re.match("([0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})?(;[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5})*$", macs))

def is_hashlist(macs):
        ##hex_digit = "[0-9A-Fa-f]"
        ##hashed_mac = "(" + hex_digit + "{96})"
        ##hash_list = hashed_mac + "?(;" + hashed_mac + ")*$"
        ##return bool(re.match(hash_list, macs))
        return bool(re.match("([0-9A-Fa-f]{96})?(;[0-9A-Fa-f]{96})*$", macs))


# returns a formatted string representing current time
def timestamp():
	return datetime.datetime.now().strftime("%D %T.%f")        

# mainly for reading blacklists and whitelists, although not restricted to such things
def read_list(filename):
	listfile = open(filename, "r")
	l = listfile.readlines()
	if l[-1] == "\n":
                l = l[:-1]
	l = [line.split("#")[0].strip() for line in l] # removes all comments (marked by preceding #) and all whitespaces
	return l

def log_write(filename, string, mode = 'a'):
        log_file = open(filename, mode)
        log_file.write(string)
        log_file.close()

def stop_monitors():
	network_file = open('/proc/net/dev', 'r')
	networks = network_file.readlines()
	network_file.close()
	monitors = [network for network in networks if re.search("mon[0-9]+", network)]

	for monitor in monitors:
		monitor_name = monitor.split(':')[0].strip()
		call(['airmon-ng', 'stop', monitor_name])
