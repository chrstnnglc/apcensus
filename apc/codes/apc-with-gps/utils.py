import datetime
import re

def timestamp():
    return datetime.datetime.now().strftime("%D %T.%f")

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