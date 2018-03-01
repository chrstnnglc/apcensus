#this will analyze the ssids of our trace files

import csv

unique_bssid = []
#these lists will contain the aps where they have a matching ssid
pldt = []
huawei = []
globe = []
smart = []
tplink = []
bayandsl = []
android = []
aztech = []
zte = []
blank = []
netgear = []
iphone = []
sky = []
evo = []
fiberhome = []
homebro = []
unidentified = []

class AP:
	def __init__(self, bssid=None, ssid=None, channel=None,enc=None):
		self.bssid = bssid
		self.ssid = ssid
		self.channel = channel
		self.enc = enc
		
#read trace file
i = 0			
with open('area2.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i != 0:		##ignore first line

			#get all data
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]

                        #only check unique aps
			if bssid not in unique_bssid:
                            new_ap = AP(bssid,ssid,channel,enc)
                            unique_bssid.append(bssid)

                            #check each ssid if it falls under the list
                            ssid_lower_case = ssid.lower()
                            if "pldt" in ssid_lower_case:
                                pldt.append(new_ap)
                            elif "huawei" in ssid_lower_case:
                                huawei.append(new_ap)
                            elif "globe" in ssid_lower_case:
                                globe.append(new_ap)
                            elif "smart" in ssid_lower_case:
                                smart.append(new_ap)
                            elif "tp-link" in ssid_lower_case:
                                tplink.append(new_ap)
                            elif "bayandsl" in ssid_lower_case:
                                bayandsl.append(new_ap)
                            elif "android" in ssid_lower_case:
                                android.append(new_ap)
                            elif "aztech" in ssid_lower_case:
                                aztech.append(new_ap)
                            elif "zte" in ssid_lower_case:
                                zte.append(new_ap)
                            elif "netgear" in ssid_lower_case:
                                netgear.append(new_ap)
                            elif "iphone" in ssid_lower_case:
                                iphone.append(new_ap)
                            elif "skybroadband" in ssid_lower_case:
                                sky.append(new_ap)
                            elif "evohotspot" in ssid_lower_case:
                                evo.append(new_ap)
                            elif "fiberhome" in ssid_lower_case:
                                fiberhome.append(new_ap)
                            elif "homebro" in ssid_lower_case:
                                homebro.append(new_ap)
                            elif "" == ssid_lower_case:
                                blank.append(new_ap)
                            else:
                                unidentified.append(new_ap)
			
		i += 1
i = 0
with open('hs_trace.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i != 0:		##ignore first line

			#get all data
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]

                        #only check unique aps
			if bssid not in unique_bssid:
                            new_ap = AP(bssid,ssid,channel,enc)
                            unique_bssid.append(bssid)

                            #check each ssid if it falls under the list
                            ssid_lower_case = ssid.lower()
                            if "pldt" in ssid_lower_case:
                                pldt.append(new_ap)
                            elif "huawei" in ssid_lower_case:
                                huawei.append(new_ap)
                            elif "globe" in ssid_lower_case:
                                globe.append(new_ap)
                            elif "smart" in ssid_lower_case:
                                smart.append(new_ap)
                            elif "tp-link" in ssid_lower_case:
                                tplink.append(new_ap)
                            elif "bayandsl" in ssid_lower_case:
                                bayandsl.append(new_ap)
                            elif "android" in ssid_lower_case:
                                android.append(new_ap)
                            elif "aztech" in ssid_lower_case:
                                aztech.append(new_ap)
                            elif "zte" in ssid_lower_case:
                                zte.append(new_ap)
                            elif "netgear" in ssid_lower_case:
                                netgear.append(new_ap)
                            elif "iphone" in ssid_lower_case:
                                iphone.append(new_ap)
                            elif "skybroadband" in ssid_lower_case:
                                sky.append(new_ap)
                            elif "evohotspot" in ssid_lower_case:
                                evo.append(new_ap)
                            elif "fiberhome" in ssid_lower_case:
                                fiberhome.append(new_ap)
                            elif "homebro" in ssid_lower_case:
                                homebro.append(new_ap)
                            elif "" == ssid_lower_case:
                                blank.append(new_ap)
                            else:
                                unidentified.append(new_ap)
			
		i += 1
i = 0
with open('tv_trace.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i != 0:		##ignore first line

			#get all data
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]

                        #only check unique aps
			if bssid not in unique_bssid:
                            new_ap = AP(bssid,ssid,channel,enc)
                            unique_bssid.append(bssid)

                            #check each ssid if it falls under the list
                            ssid_lower_case = ssid.lower()
                            if "pldt" in ssid_lower_case:
                                pldt.append(new_ap)
                            elif "huawei" in ssid_lower_case:
                                huawei.append(new_ap)
                            elif "globe" in ssid_lower_case:
                                globe.append(new_ap)
                            elif "smart" in ssid_lower_case:
                                smart.append(new_ap)
                            elif "tp-link" in ssid_lower_case:
                                tplink.append(new_ap)
                            elif "bayandsl" in ssid_lower_case:
                                bayandsl.append(new_ap)
                            elif "android" in ssid_lower_case:
                                android.append(new_ap)
                            elif "aztech" in ssid_lower_case:
                                aztech.append(new_ap)
                            elif "zte" in ssid_lower_case:
                                zte.append(new_ap)
                            elif "netgear" in ssid_lower_case:
                                netgear.append(new_ap)
                            elif "iphone" in ssid_lower_case:
                                iphone.append(new_ap)
                            elif "skybroadband" in ssid_lower_case:
                                sky.append(new_ap)
                            elif "evohotspot" in ssid_lower_case:
                                evo.append(new_ap)
                            elif "fiberhome" in ssid_lower_case:
                                fiberhome.append(new_ap)
                            elif "homebro" in ssid_lower_case:
                                homebro.append(new_ap)
                            elif "" == ssid_lower_case:
                                blank.append(new_ap)
                            else:
                                unidentified.append(new_ap)
			
		i += 1
i = 0
with open('log-76.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i != 0:		##ignore first line

			#get all data
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]

                        #only check unique aps
			if bssid not in unique_bssid:
                            new_ap = AP(bssid,ssid,channel,enc)
                            unique_bssid.append(bssid)

                            #check each ssid if it falls under the list
                            ssid_lower_case = ssid.lower()
                            if "pldt" in ssid_lower_case:
                                pldt.append(new_ap)
                            elif "huawei" in ssid_lower_case:
                                huawei.append(new_ap)
                            elif "globe" in ssid_lower_case:
                                globe.append(new_ap)
                            elif "smart" in ssid_lower_case:
                                smart.append(new_ap)
                            elif "tp-link" in ssid_lower_case:
                                tplink.append(new_ap)
                            elif "bayandsl" in ssid_lower_case:
                                bayandsl.append(new_ap)
                            elif "android" in ssid_lower_case:
                                android.append(new_ap)
                            elif "aztech" in ssid_lower_case:
                                aztech.append(new_ap)
                            elif "zte" in ssid_lower_case:
                                zte.append(new_ap)
                            elif "netgear" in ssid_lower_case:
                                netgear.append(new_ap)
                            elif "iphone" in ssid_lower_case:
                                iphone.append(new_ap)
                            elif "skybroadband" in ssid_lower_case:
                                sky.append(new_ap)
                            elif "evohotspot" in ssid_lower_case:
                                evo.append(new_ap)
                            elif "fiberhome" in ssid_lower_case:
                                fiberhome.append(new_ap)
                            elif "homebro" in ssid_lower_case:
                                homebro.append(new_ap)
                            elif "" == ssid_lower_case:
                                blank.append(new_ap)
                            else:
                                unidentified.append(new_ap)
			
		i += 1
i = 0
with open('trace_01312018.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
		if i != 0:		##ignore first line

			#get all data
			bssid = line[0]
			ssid = line[1]
			enc = line[2]
			channel = line[3]

                        #only check unique aps
			if bssid not in unique_bssid:
                            new_ap = AP(bssid,ssid,channel,enc)
                            unique_bssid.append(bssid)

                            #check each ssid if it falls under the list
                            ssid_lower_case = ssid.lower()
                            if "pldt" in ssid_lower_case:
                                pldt.append(new_ap)
                            elif "huawei" in ssid_lower_case:
                                huawei.append(new_ap)
                            elif "globe" in ssid_lower_case:
                                globe.append(new_ap)
                            elif "smart" in ssid_lower_case:
                                smart.append(new_ap)
                            elif "tp-link" in ssid_lower_case:
                                tplink.append(new_ap)
                            elif "bayandsl" in ssid_lower_case:
                                bayandsl.append(new_ap)
                            elif "android" in ssid_lower_case:
                                android.append(new_ap)
                            elif "aztech" in ssid_lower_case:
                                aztech.append(new_ap)
                            elif "zte" in ssid_lower_case:
                                zte.append(new_ap)
                            elif "netgear" in ssid_lower_case:
                                netgear.append(new_ap)
                            elif "iphone" in ssid_lower_case:
                                iphone.append(new_ap)
                            elif "skybroadband" in ssid_lower_case:
                                sky.append(new_ap)
                            elif "evohotspot" in ssid_lower_case:
                                evo.append(new_ap)
                            elif "fiberhome" in ssid_lower_case:
                                fiberhome.append(new_ap)
                            elif "homebro" in ssid_lower_case:
                                homebro.append(new_ap)
                            elif "" == ssid_lower_case:
                                blank.append(new_ap)
                            else:
                                unidentified.append(new_ap)
			
		i += 1

print "Total APS: " + str(len(unique_bssid))
print "PLDT: " + str(len(pldt))
print "HUAWEI: " + str(len(huawei))
print "GLOBE: " + str(len(globe))
print "SMART: " + str(len(smart))
print "TP-LINK: " + str(len(tplink))
print "BAYANDSL: " + str(len(bayandsl))
print "ANDROID: " + str(len(android))
print "AZTECH: " + str(len(aztech))
print "ZTE: " + str(len(zte))
print "NETGEAR: " + str(len(netgear))
print "IPHONE: " + str(len(iphone))
print "SKYBROADBAND: " + str(len(sky))
print "EVOHOTSPOT: " + str(len(evo))
print "FIBERHOME: " + str(len(fiberhome))
print "HOMEBRO: " + str(len(homebro))
print "NO NAME: " + str(len(blank))
print "UNIDENTIFIED: " + str(len(unidentified))


with open('group_ssid.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')

    write_file.writerow(["Total APs",str(len(unique_bssid))])
    write_file.writerow(["PLDT",str(len(pldt))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in pldt:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])
    write_file.writerow(["Huawei",str(len(huawei))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in huawei:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])   
    write_file.writerow(["Globe",str(len(globe))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in globe:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["Smart",str(len(smart))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in smart:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["TP-Link",str(len(tplink))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in tplink:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["BayanDSL",str(len(bayandsl))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in bayandsl:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["Android",str(len(android))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in android:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["Aztech",str(len(aztech))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in aztech:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["ZTE",str(len(zte))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in zte:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["Netgear",str(len(netgear))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in netgear:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["iPhone",str(len(iphone))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in iphone:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["Sky Broadband",str(len(sky))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in sky:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["EVO HotSpot",str(len(evo))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in evo:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["Fiber Home",str(len(fiberhome))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in fiberhome:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["HomeBro",str(len(homebro))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in homebro:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["No Name",str(len(blank))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in blank:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])

    write_file.writerow([""])    
    write_file.writerow(["Unidentified",str(len(unidentified))])
    write_file.writerow(["BSSID","SSID","Encryption","Channel"])
    for item in unidentified:
        write_file.writerow([str(item.bssid),str(item.ssid),str(item.enc),str(item.channel)])
    
