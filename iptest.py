#!/usr/bin/python
from subprocess import *
from time import sleep, strftime
from datetime import datetime


cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"

def run_cmd(cmd):
        p = Popen(cmd, shell=True, stdout=PIPE)
        output = p.communicate()[0]
        return output

while 1:
        ipaddr = run_cmd(cmd)
        print ('IP %s' % ( ipaddr ))
        sleep(10)
