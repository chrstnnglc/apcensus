from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
import datetime
import math

import constants
from utility_methods import *
from monitor import MonitorThread

# Slave class, which waits for a signal from the master to send it information on all the macs collected in "this window"
class Slave(LineReceiver):
	def __init__(self, factory):
		self.factory = factory
	def lineReceived(self, data):
		# when the master requests the current window from this unit
		if data == "sendplz":
                        print("got sendplz")
                        self.sendLine("len:%d"%(math.ceil(len(self.factory.window_umacs) / constants.max_macs)))
		elif data == "ok then":
                        for i in range(0, len(self.factory.window_umacs), constants.max_macs):
                                self.sendLine(";".join(self.factory.window_umacs[i:i+constants.max_macs]))
			del self.factory.window_umacs[:]
                else:
                        print("OTHER DATA: " + str(data))
                
class Slavery(ClientFactory): # Slave Factory
	def __init__(self, log_folder, interface, gps = None):
		self.log_folder = log_folder
		self.is_connected = False
		
		self.window_umacs = [] # list of unique macs in the latest window
                self.previous_t = datetime.datetime.now()
		self.slave = Slave(self)
		
		self.m = MonitorThread(self, interface, gps = gps)
	
	def startedConnecting(self, connector):
		print('Started to connect.')

	def buildProtocol(self, addr):
		print('Connected.')
		self.is_connected = True
		self.m.start()
		return self.slave
	
	def clientConnectionLost(self, connector, reason):
		print('Lost connection.  Reason:' + str(reason))
		self.is_connected = False
		dc_notif = open("dc on " + timestamp(),"w")
                dc_notif.write("disconnected on --- " + timestamp())
		if self.m.isAlive():
			print("Waiting for threads to stop first.")
			self.m.join()
		if reactor.running:
			reactor.stop()

	def clientConnectionFailed(self, connector, reason):
		print('Connection failed. Reason:' + str(reason))
		self.is_connected = False
		if self.m.isAlive():
			print("Waiting for threads to stop first.")
			self.m.join()
		if reactor.running:
			reactor.stop()
