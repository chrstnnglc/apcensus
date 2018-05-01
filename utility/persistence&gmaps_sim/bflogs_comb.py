#This appends all bflog.txt from different readings and creates a file that
#contains all of them

res_file = open("bflog_readings.txt","a+")
ap_file = open("bflog.txt","r")

for line in ap_file:
    parsed = line.split()
    gps_date = parsed[0] + " " + parsed[1]
    others = parsed[6] + " " + parsed[7] + " " + parsed[8] + " " + parsed[9] + " " + parsed[10] + " " + parsed[11]
    text = gps_date + " >> " + others + "\n"
    res_file.write(text)

ap_file.close()
res_file.close()
