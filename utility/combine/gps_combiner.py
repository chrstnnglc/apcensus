#This combines all the gps readings and lists them in 1 big file
#we will input the gps_readings.txt file for each reading 1 by 1
import datetime

def rpi_time_convert(time_in):
        formatto = "%Y-%m-%d %H:%M:%S.%f"
        formatfrom = "%m/%d/%y %H:%M:%S.%f"
        time_out = datetime.datetime.strptime(time_in,formatfrom)
        time_out = time_out.strftime(formatto)
        return time_out

def gps_time_convert(time_in):
        formatto = "%Y-%m-%d %H:%M:%S"
        formatfrom = "%m/%d/%Y %H:%M:%S"
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
    gps_time = gps_time_convert(parsed[0] + " " + parsed[1])
    time_capt = rpi_time_convert(parsed[3] + " " + parsed[4]) 
    lat = parsed[6]
    lat = lat[:-1]
    lng = parsed[7]
    text = gps_time + "|" + time_capt + "|" + lat + "|" + lng + "\n"
    master_file.write(text)
gps_file.close()
master_file.close()
