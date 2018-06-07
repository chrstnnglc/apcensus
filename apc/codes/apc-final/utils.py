import datetime
from datetime import timedelta
import re

def timestamp():
    return datetime.datetime.now().strftime("%D %T.%f")

#converts the gps time (UTC to GMT)
def get_time(gps_time):
    formatfrom = "%Y-%m-%dT%H:%M:%S"
    formatto = "%m/%d/%Y %H:%M:%S"
    if gps_time != "":     #this condition prevents error when we try to write time in text files while gps is still offline  
        newgps = datetime.datetime.strptime(gps_time[0:19],formatfrom)
        newgps = newgps + timedelta(hours = 8) #we add 8 hours to gps time to match the timezone with Asia/Manila
        newgps = newgps.strftime(formatto)
        return newgps
    else:
        return ""

# determines whether the string conforms to the "log-N" format
def is_log(log):
        return re.match("log-[0-9]+$", log)

# returns only the number of the log (removes the initial "log-" of "log-N" and returns N)
# assumes the form has been validated previously
def get_log_number(log):
        return int(log[4:])

def log_write(filename, string, mode = 'a'):
        log_file = open(filename, mode)
        log_file.write(string)
        log_file.close()
