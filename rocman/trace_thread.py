#!/usr/bin/python

from subprocess import call
import threading
import thread
import time

exitFlag = 0

class SharkThread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		call (['sudo','ifconfig','wlan1','down'])
		call (['sudo','iwconfig','wlan1','mode','monitor'])
		call (['sudo','ifconfig','wlan1','up'])
		call(['sudo', 'tcpdump', '-i', 'wlan1', '-e', '-s', '256', '-w', 'trace.pcap', 'type', 'mgt'])

try:
	shark = SharkThread()
	shark.start()
except:
	print "Error: unable to start thread"
	raise
while 1:
	pass