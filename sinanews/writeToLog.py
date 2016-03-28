import os
import time
 #log function: when program show wrong information we will use this function to record the error.
def error_log(text):
    ISOTIMEFORMAT = '%Y-%m-%d %X'
    date = time.strftime(ISOTIMEFORMAT, time.localtime(time.time()))
    error = "%s\n" % (text + "     time:" + date)
    if os.path.exists(logfile):
        file = open(logfile, 'a')
    elif os.path.exists(os.path.dirname(logfile)):
        file = open(logfile, 'w')
    else:
        os.makedirs(os.path.dirname(logfile), mode=755)
        file = open(logfile, 'w')
        file.write(error)
        file.close()
