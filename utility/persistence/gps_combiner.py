#This combines all the gps readings and lists them in 1 big file
#we will input the gps_readings.txt file for each reading 1 by 1
import datetime

def convert_time_format(time_in):
        formatto = "%Y-%m-%d %H:%M:%S.%f"
        formatfrom = "%m/%d/%Y %H:%M:%S.%f"
        time_out = datetime.datetime.strptime(time_in,formatfrom)
        time_out = time_out.strftime(formatto)
        return time_out

gps_file = open("gps_readings.txt","r")
master_file = open("master_gps.txt","a+")
for line in gps_file:
    parsed = line.split()
    for i in range(0,len(parsed)):
        parsed[i] = parsed[i].strip()

    #we get the time of rpi
    time_read = convert_time_format(parsed[3] + " " + parsed[4])
    lat = parsed[6]
    lat = lat[:-1]
    lng = parsed[7]
    out_text = time_read + "|" + lat + "|" + lng + "\n"
    master_file.write(out_text)
    

gps_file.close()
master_file.close()
