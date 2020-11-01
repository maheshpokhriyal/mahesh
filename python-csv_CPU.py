import os
import subprocess
import os.path
import psutil
import numpy as np
import pandas as pd
import csv
from collections import OrderedDict

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

v_phy=(f"  {psutil.cpu_count(logical=False)}")
v_core=(f"  {psutil.cpu_count(logical=True)}")

def cpuinfo():
    cpuinfo=OrderedDict()
    procinfo=OrderedDict()
    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs=nprocs+1
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
        cpumodel=(f" {cpuinfo[processor]['model name']}")


fields = ['Hostname', 'CPU Model', 'Physical Cores', 'Total Cores' ]
# data rows of csv file
rows = [[f""+str(hostname1), (f""+str(cpumodel)), f""+str(v_phy), f""+str(v_core) ]]

# name of csv file
filename = "CSV_OUTPUT_NEW_N/CPU_INFO.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
