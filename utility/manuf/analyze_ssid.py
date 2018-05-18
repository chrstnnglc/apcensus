#this will analyze the ssids of our trace files
from oui_dict import *
import csv

ap_list = []
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
netgear = []
iphone = []
sky = []
evo = []
fiberhome = []
homebro = []
unidentified = []

#these lists will contain the aps where they have the same type
fib_list = []
bb_list = []
mbb_list = []
hs_list = []
phone_list = []
nap_list = []
uni_list = []

#these lists will contain the classification of internet based on manufacturer
fiber = ["Fiberhom"]
broadband = []
mobile_bb = ["GreenPac"]
hotspot = ["TctMobil"]
phone = ["SamsungE","Apple","VivoMobi","Nokia","SianoMob","RapidMob","Longchee","Microsof","SenaoInt","Guangdon","BlackBer"]
none_ap = ["HewlettP","Roku","Mxchip","Micro-St","Bose","Guangzho","Raspberr"]

#these lists will contain the classification of internet based on SSID
fiber2 = []
broadband2 = ["PLDTHOMEDSL", "PLDTMyDSL", "ZTEH108N", "SKYbroadband", "NetgearORBI"]
mobile_bb2 = ["HomeBro_ULTERA", "HUAWEI-E5172", "HUAWEI-B315"]
hotspot2 = ["EVOHOTSPOT", "EVO WIFI HOTSPOT", "EVOLUTION PREPAID HOT SPOT", "ZTE-MF65M", "Globe_LTE MIFI", "HUAWEI-E5330", "HUAWEI-E5372", "HUAWEI-E5220", "HUAWEI-E5373", "HUAWEI-E5336"]
phone2 = ["HUAWEI Y541", "HUAWEI GR5", "HUAWEI Y7", "HUAWEI P9", "HUAWEI P10", "AndroidAP", "AndroidHotspot", "iPhone"]
none_ap2 = ["YICarCam", "Mitsubishi Wireless TV", "BRAVIA", "DashCamStealth"]

#this will contain the list of manufacturers wherein we have no guess yet
unid_manuf = []

class AP:
	def __init__(self, gps_time=None, time_capt=None, mac=None, ssid=None, sec=None, rssi=None, ch=None, manuf=None, ap_type=None,lat=None, lng=None,):
                self.gps_time = gps_time
                self.time_capt = time_capt
		self.mac = mac
		self.ssid = ssid
		self.security = sec
		self.rssi = rssi
		self.channel = ch
		self.manuf = manuf
		self.ap_type = ap_type
		self.lat = lat
		self.lng = lng

#check AP's ssid if it falls under the list
#these are the default SSIDs that we know so far
def brand_check(ssid):
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
        else:
                unidentified.append(new_ap)

def type_check(manuf,ssid,mac):
		if manuf in fiber:
			return "Fiber"
		elif manuf in broadband:
			return "Broadband"
		elif manuf in mobile_bb:
			return "Mobile broadband"
		elif manuf in hotspot:
			return "Hotspot"
		elif manuf in phone:
			return "Phone"
		elif manuf in none_ap:
			return "Not an AP"
		else:
                        if "bayandsl" in ssid.lower():
                                return "Broadband"
                        for txt in fiber2:
                                if txt in ssid:
                                        return "Fiber"
                        for txt in broadband2:
                                if txt in ssid:
                                        return "Broadband"
                        for txt in mobile_bb2:
                                if txt in ssid:
                                        return "Mobile broadband"
                        for txt in hotspot2:
                                if txt in ssid:
                                        return "Hotspot"
                        for txt in phone2:
                                if txt in ssid:
                                        return "Phone"
                        for txt in none_ap2:
                                if txt in ssid:
                                        return "Not an AP"
                        
                return "Unidentified"

def group_type(ap_type):
        if ap_type == "Fiber":
                fib_list.append(new_ap)
        elif ap_type == "Broadband":
                bb_list.append(new_ap)
        elif ap_type == "Mobile broadband":
                mbb_list.append(new_ap)
        elif ap_type == "Hotspot":
                hs_list.append(new_ap)
        elif ap_type == "Phone":
                phone_list.append(new_ap)
        elif ap_type == "Not an AP":
                nap_list.append(new_ap)
        elif ap_type == "Unidentified":
                uni_list.append(new_ap)

#Initialize APs we need to analyze                
i = 0
with open('gtl2_list.csv','rb') as csvfile:
	reader = csv.reader(csvfile, delimiter=',', quotechar='"')
	for line in reader:
                if i != 0:		##ignore first line

			#get all data
                        gps_time = line[0]
                        time_capt = line[1]
                        mac = line[2]
                        ssid = line[3]
                        sec = line[4]
                        rssi = line[5]
                        ch = line[6]
                        manuf = line[7]
                        ap_type = line[8]
                        lat = line[9]
                        lng = line[10]
                        #check the type of ap
                        ap_type = type_check(manuf,ssid,mac)
                        new_ap = AP(gps_time,time_capt,mac,ssid,sec,rssi,ch,manuf,ap_type,lat,lng)
                        ap_list.append(new_ap)
                        #check each ssid if it falls under the list
                        brand_check(ssid)
                        #group ap according to type
                        group_type(ap_type)
			
		i += 1

print "Total APS: " + str(len(ap_list))
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
print "UNIDENTIFIED: " + str(len(unidentified))

print "\nTYPES"
print "FIBER: " + str(len(fib_list))
print "BROADBAND: " + str(len(bb_list))
print "MOBILE BROADBAND: " + str(len(mbb_list))
print "HOTSPOT: " + str(len(hs_list))
print "PHONE: " + str(len(phone_list))
print "NOT AP: " + str(len(nap_list))
print "UNIDENTIFIED: " + str(len(uni_list))

#make a csv file wherein APs are grouped up according to brand(default ssid)
with open('gtl2_brand.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')

    write_file.writerow(["Total APs",str(len(ap_list))])
    write_file.writerow(["PLDT",str(len(pldt))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in pldt:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])
    write_file.writerow(["Huawei",str(len(huawei))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in huawei:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])   
    write_file.writerow(["Globe",str(len(globe))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in globe:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["Smart",str(len(smart))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in smart:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["TP-Link",str(len(tplink))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in tplink:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["BayanDSL",str(len(bayandsl))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in bayandsl:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["Android",str(len(android))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in android:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["Aztech",str(len(aztech))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in aztech:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["ZTE",str(len(zte))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in zte:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["Netgear",str(len(netgear))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in netgear:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["iPhone",str(len(iphone))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in iphone:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["Sky Broadband",str(len(sky))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in sky:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["EVO HotSpot",str(len(evo))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in evo:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["Fiber Home",str(len(fiberhome))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in fiberhome:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["HomeBro",str(len(homebro))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in homebro:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

    write_file.writerow([""])    
    write_file.writerow(["Unidentified",str(len(unidentified))])
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in unidentified:
        write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

#make a csv file wherein APs are grouped up according to type
with open('gtl2_type.csv','wb') as csvfile:
        write_file = csv.writer(csvfile, delimiter = ',')
        
        write_file.writerow(["Total APs",str(len(ap_list))])
        write_file.writerow(["Fiber",str(len(fib_list))])
        write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in fib_list:
                write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

        write_file.writerow([""])
        write_file.writerow(["Broadband",str(len(bb_list))])
        write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in bb_list:
                write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

        write_file.writerow([""])
        write_file.writerow(["Mobile broadband",str(len(mbb_list))])
        write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in mbb_list:
                write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

        write_file.writerow([""])
        write_file.writerow(["Hotspot",str(len(hs_list))])
        write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in hs_list:
                write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

        write_file.writerow([""])
        write_file.writerow(["Phone",str(len(phone_list))])
        write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in phone_list:
                write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

        write_file.writerow([""])
        write_file.writerow(["Non AP",str(len(nap_list))])
        write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in nap_list:
                write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

        write_file.writerow([""])
        write_file.writerow(["Unidentified",str(len(uni_list))])
        write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
        for item in uni_list:
                write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])

#make a csv file of master list
with open('gtl2_list.csv','wb') as csvfile:
    write_file = csv.writer(csvfile, delimiter = ',')
    write_file.writerow(["GPS Time","Time","MAC","SSID","Encryption","RSSI","Channel","Manufacturer","AP Type","Latitude","Longitude"])
    for item in ap_list:
            write_file.writerow([str(item.gps_time),str(item.time_capt),str(item.mac),str(item.ssid),str(item.security),str(item.rssi),str(item.channel),str(item.manuf),str(item.ap_type),str(item.lat),str(item.lng)])	

#make a text file of master list
res_file = open("gtl2_list.txt",'w')
for item in ap_list:
	text = 	str(item.gps_time) +"|"+ str(item.time_capt) +"|"+ str(item.mac) +"|"+ str(item.ssid) +"|"+ str(item.security) +"|"+ str(item.rssi) +"|"+ str(item.channel) +"|"+ str(item.manuf) +"|"+ str(item.ap_type) +"|"+ str(item.lat) +"|"+ str(item.lng) + "\n"
	res_file.write(text)
res_file.close()
