#!/usr/bin/python3
import psutil
import platform
import os
import subprocess
import sys
import re
import time
import getpass
import os.path
import datetime
import socket
from collections import OrderedDict
from datetime import date


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

############ OS ##############################
hostname = socket.gethostname()
serial = subprocess.getoutput('dmidecode -s system-serial-number')
hw = subprocess.getoutput('dmidecode -s system-product-name')
kernel = subprocess.getoutput('uname -r')
uname=platform.uname()
## uptime ##
with open("/proc/uptime","r") as f:
    uptime=f.read().split(" ")[0].strip()
uptime=int(float(uptime))
uptime_hours=uptime//3600
uptime_minutes=(uptime % 3600) //60


#### Processor #######

v_phy=(f"{psutil.cpu_count(logical=False)}")
v_core=(f"{psutil.cpu_count(logical=True)}")
cpufreq = psutil.cpu_freq()
v_fre=(f" Current Frequency: {cpufreq.current:.2f}Mhz")

def cpuinfo():
	cpuinfo=OrderedDict()
	procinfo=OrderedDict()

	nprocs = 0
	with open('/proc/cpuinfo') as f:
		for line in f:
			if not line.strip():
                		# end of one processor
				cpuinfo['proc%s' % nprocs] = procinfo
				nprocs=nprocs+1
                		# Reset
				procinfo=OrderedDict()
			else:
				if len(line.split(':')) == 2:
					procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
				else:
					procinfo[line.split(':')[0].strip()] = ''
	return cpuinfo

if __name__=='__main__':
	cpuinfo = cpuinfo()
	for processor in cpuinfo.keys():
		cpumodel=(f"Processor: {cpuinfo[processor]['model name']}")

########### Disk Info ####################

partitions = psutil.disk_partitions()
for partition in partitions:
    s2=""+str(partition.mountpoint)+"\n"
    with open("FS.txt","a") as wh:
        wh.write(s2)
    wh.close()
f = open("FS.txt","r+")
disk=os.popen("cat FS.txt").read()
f.truncate(0)

###############################################################

vg=os.popen("vgs").read()
with open("vg.txt","w") as wh:
    wh.write(vg)
    wh.close()
v = open("vg.txt","r")
for line in v:
    fields = line.split()
    f1=fields[5]
    f2 = ""+str(f1)+""
    f3 = ""+str(f2.replace('<', ' ').replace('VSize',' '))+""
v.close()

########### Memory ###################
svmem=psutil.virtual_memory()


import csv  
    
# field names  
fields = ['HostName', 'OS', 'Serial number', 'IP Address', 'OS Kernel', 'CPU core count', 'CPU speed (MHz)', 'Disk space (GB)', 'Mount Point', 'RAM' ]
# data rows of csv file
rows = [[(f"{uname.node}"), (f""+str(platform.linux_distribution())), f""+str(serial), f"{socket.gethostbyname(hostname)}", f""+str(kernel), f""+str(v_phy), (f"{cpuinfo[processor]['model name']}"), f""+str(f3), f""+str(disk), (f"{get_size(svmem.total)}")]] 

# name of csv file
filename = "CSV_OUTPUT_NEW_N/Server_Info.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
