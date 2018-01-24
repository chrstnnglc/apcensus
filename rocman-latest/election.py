from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory, ClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint, TCP4ClientEndpoint, connectProtocol
from subprocess import call, check_output, Popen
import gps
import time
import sys

import script_argparser
import constants
from utility_methods import *

def adhoc_collect():
	frens = []
	o = check_output(["sudo",  "arp-scan", "-I", "wlan0", "-l"])
	for k in o.split("\n"):
	    for z in k.split('\t'):
		if is_ip(z):
			frens.append(z)
	return frens

class Responder(Protocol):
	def dataReceived(self, data):
		global dominance
		clean_data = str(data.strip())
		if clean_data == "check" and dominance != "undef":
			print("i do a send")
			self.transport.write(dominance)
		elif clean_data == "check":
                        print("got check but dominance is %s"%(dominance))
		else:
                        print("got weird data: " + clean_data)
		
class ResponderFactory(Factory):
	def buildProtocol(self, addr):
		return Responder()

class Poller(Protocol):
	def connectionMade(self):
		self.transport.write("check")
	def dataReceived(self, data):
                global bois, dominance
                clean_data = data.strip()
                if clean_data == "undef":
                        print("recieved undef, rechecking")
                        self.transport.write("check")
                else:
                        bois[str(self.transport.getPeer().host)] = data
                        boi_states = bois.values()
                        print(bois)
                        if "undef" not in boi_states:
                                if "master" in boi_states:
                                        dominance = "slave"
                                        for boi, state in bois.iteritems():
                                               if state == "master":
                                                       president = boi
                                        Popen(['lxterminal', '-e', 'sudo python %smain.py --slave %s '%(constants.file_directory, president) + " ".join(sys.argv[1:])])
                                        print("client started, associated to master: %s"%(president))
                                else:
                                        print("there is no viable master, rip")
		
class PollerFactory(ClientFactory):
	def startedConnecting(self, connector):
		print("Started to connect.")
	def buildProtocol(self, addr):
		print("Connected.")
		return Poller()
	def clientConnectionFailed(self, connector, reason):
                global connections_failed, bois, is_ffd, dominance
                print('Connection failed. Reason:', reason)
                connections_failed += 1
                if connections_failed == len(bois) and is_ffd:
                        dominance = "master"
                        Popen(['lxterminal', '-e', 'sudo python %smain.py --master '%(constants.file_directory) + " ".join(sys.argv[1:])])
                        print("master started")

if __name__ == "__main__":
        parser = script_argparser.get_parser(role_check = False)
        args = parser.parse_args()
        gps_not_needed = args.ignore_gps
        global bois, is_ffd, connections_failed, dominance
	##print("[NOTE] Do not start this in IDLE as it will not handle subprocess.call correctly.\n(it will wait until the other terminal is closed)")

	has_internet = True # [TODO] Make an actual check
	try:
		session = gps.gps("localhost", "2947")
		session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
		gpsd_info = session.next()
		device_info = session.next()
		device_info = device_info.__dict__['devices']
		has_gps = bool([info for info in device_info[0].keys() if info not in ['path', 'class']])
	except:
		# [TODO] Specify error type in code
                # [TODO] Start the gps and redo instead
		print("[ERROR] start the fucking gps")
		exit()
	is_ffd = has_internet and (has_gps or gps_not_needed)

	dominance = "undef"
	bois = {}
	for ip in adhoc_collect():
		bois[ip] = "undef"
	resp = ResponderFactory()
        resp_end = TCP4ServerEndpoint(reactor, 8111)
        resp_end.listen(resp)
	connections_failed = 0
	if bois:       
                for boi in bois.keys():
                        poll =  PollerFactory()
                        reactor.connectTCP(boi, 8111, poll)
                        print("connecting to " + boi)
        elif is_ffd:
                print("adhoc network is empty")
                dominance = "master"                
                Popen(['lxterminal', '-e', 'sudo python %smain.py --master '%(constants.file_directory) + " ".join(sys.argv[1:])])
                print("master started")
        else:
                print(";__;") # not ffd but also noone else
                # [TODO] Wait for a master to show up
	print("running reactor")
	reactor.run()
	
