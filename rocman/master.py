from twisted.internet import reactor
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols.basic import LineReceiver
from twisted.protocols.policies import TimeoutMixin
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
import datetime

#import os.path
import settings
import constants
from utility_methods import *
from monitor import MonitorThread

##TEMPORARY VARIABLE
MRT_RANGEDEVICES = ["14:1f:78:0b:22:bc","ac:5f:3e:4c:f6:13"]

class Master(LineReceiver,TimeoutMixin):
        def __init__(self, factory):
                self.factory = factory
                self.mac_batches_to_receive = 0
                self.mac_batches_received = 0
                self.macs_so_far = []

        def connectionMade(self):
                self.factory.slaves.append(self)
                self.setTimeout(settings.window_size+15)
                pi_connected_message = "There are currently %d connected pis.\n" % (len(self.factory.slaves))
                print(pi_connected_message)

        def connectionLost(self, reason):
                print("Connection to a pi was lost")
                dc_notif = open(log_folder+"disconnects.txt","a+")
                dc_notif.write("disconnected on --- " + timestamp()+"\n")
                dc_notif.close()
                self.factory.killFactory()
        def timeoutConnection(self):
                print("TIMEOUT")
                dc_notif = open(log_folder+"disconnects.txt","a+")
                dc_notif.write("lost a slave on --- " + timestamp()+"\n")
                dc_notif.close()
                self.factory.killFactory()
        def lineReceived(self, data):
                # [NOTE]
                # finishing the window is dependent on the master being able to recieve data from all the slaves before the next window
                # i think this assumption is acceptable, but if this assumption should fail this code will have problems
                self.resetTimeout()
                if data[:4] == "len:":
                        self.mac_batches_to_receive = int(data[4:])
                        self.sendLine("ok then")
                elif is_valid_list(data):
                        print("MACS RECIEVED: " + str(data))
                        self.macs_so_far += data.split(";")
                        self.mac_batches_received += 1
                        if self.mac_batches_received >= self.mac_batches_to_receive:
                                self.factory.macs_recieved.append(self.macs_so_far)
                                del self.macs_so_far[:]
                                self.mac_batches_received = 0
                                self.mac_batches_to_receive = 0
                                if len(self.factory.macs_recieved) >= len(self.factory.slaves):
                                        self.factory.finishWindow()
                else:
                        print("OTHER DATA: " + str(data))
                
class Mastery(Factory):
        def __init__(self, log_folder, interface, gps):
                self.is_connected = False
                self.log_folder = log_folder
                self.gps = gps
                
                self.slaves = [] # list of Master instances, each instance ties to one slave
                
                self.window_umacs = []
                self.macs_recieved = []
                self.windowed_log_location = log_folder + 'windowed-%g.txt'%(settings.window_size)
                self.windowed_macs_location = log_folder + 'windowed_macs-%g.txt'%(settings.window_size)
                self.total_windowed_log_location = log_folder + 'total_windowed-%g.txt'%(settings.window_size)
                self.total_windowed_macs_location = log_folder + 'total_windowed_macs-%g.txt'%(settings.window_size)

                self.m = MonitorThread(self, interface, gps = gps)

                if settings.server_ip:
                        self.server_connection = ServerConnection()
                        server_endpoint = TCP4ClientEndpoint(reactor, settings.server_ip, 8006)
                        #d = server_endpoint.connect(ServerConnectionFactory())
                        connectProtocol(server_endpoint, self.server_connection)
                
                self.startScanning()
                
        def buildProtocol(self, addr):
                return Master(self)

        def startScanning(self):
                self.is_connected = True
                self.m.start()
                self.previous_t = datetime.datetime.now()
                self.startNextWindow()

        def startNextWindow(self):
                reactor.callLater(settings.window_size, self.requestWindow)

        # sends a request to all slaves (if applicable) to ask for their current window info
        def requestWindow(self):
                if self.slaves:
                        for slave in self.slaves:
                                slave.sendLine("sendplz")
                else:
                        self.finishWindow() # will simply finish the window if there is nothing to wait for

        # finishes up a window once everything has been finished
        def finishWindow(self):
                now = datetime.datetime.now()

                # writes to the logs for the non-aggregated window info
                log_write(self.windowed_log_location, "%s to %s >> %d unique macs, (%f, %f)\n"%(
                        self.previous_t.strftime("%D %T.%f"),
                        now.strftime("%D %T.%f"),
                        len(self.window_umacs),
                        self.gps.lat,
                        self.gps.lon))
                log_write(self.windowed_macs_location, "%s,%s->"%(self.gps.lat, self.gps.lon) + "|".join(self.window_umacs) + "\n")

                # creates a list of all the unique macs seen by all devices of this network
                total_umacs = self.window_umacs
                for macs in self.macs_recieved:
                        total_umacs = total_umacs + macs
                total_umacs = list(set(total_umacs))

                # refreshes the list of macs in the window
                del self.macs_recieved[:]
                del self.window_umacs[:]

                # writes to the logs for the aggregated window info
                log_write(self.total_windowed_log_location, "%s to %s >> %d unique macs, (%f, %f)\n"%(
                        self.previous_t.strftime("%D %T.%f"),
                        now.strftime("%D %T.%f"),
                        len(total_umacs),
                        self.gps.lat,
                        self.gps.lon))
                log_write(self.total_windowed_macs_location, "%s,%s->"%(self.gps.lat, self.gps.lon) + "|".join(total_umacs) + "\n")

                # sends the data to the server
                if settings.server_ip:
                        try:
                                self.server_connection.sendData("%d|%f,%f"%(len(total_umacs), self.gps.lat, self.gps.lon))
                                print(total_umacs)
                                for k in MRT_RANGEDEVICES:
                                        if k in total_umacs:
                                                self.server_connection.sendData(" --- phone home")
                        except:
                                print("server machine broke")
                # queues up the next window
                self.startNextWindow()
                self.previous_t = now

        def killFactory(self):
                # set the variable which will stop the threads from looping
                self.is_connected = False
                # wait for the threads to stop
                if self.m.isAlive():
                        print("Waiting for threads to stop first.")
                        self.m.join()
                # stop the reactor
                if reactor.running:
                        reactor.stop()

class DistWinMastery(Mastery):
        def __init__(self, log_folder, interface, gps):
                self.last_loc = (gps.lat, gps.lon)
                Mastery.__init__(self, log_folder, interface, gps)

        def startNextWindow(self):
                reactor.callLater(1.0, windowLoop)

        def windowLoop(self):
                if sq_dist(curr_loc, self.last_loc) > settings.dist_thresh:
                        self.factory.requestWindow()
                        self.last_loc = curr_loc
                else:
                        reactor.callLater(1.0, self.windowLoop)
        

# A very bare-bones class which connects to the server to send readings to
class ServerConnection(Protocol):
        def sendData(self, data):
                self.transport.write(data)

"""
# A factory for said class which connects to the server to send readings to
class ServerConnectionFactory(ReconnectingClientFactory):
        def buildProtocol(self):
                return ServerConnection(self)
"""
        
