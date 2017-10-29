# takes in the beacons.txt file from rocman and checks if each BSSID is in the wigle file

filename = raw_input("Enter the beacons file name: ")
bfile = open(filename, 'r')

filename = raw_input("Enter the JSON data file name: ")
wigledata = open(filename).read()

for bssid in bfile:

	if bssid.upper().strip("\n") in wigledata:
		print bssid