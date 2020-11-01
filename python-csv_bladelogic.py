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
import csv
import subprocess
import os
import os.path
from os import path
from pathlib import Path
from subprocess import Popen, PIPE
from datetime import date

    
bladelogic=os.popen("rpm -qa |grep BladeLogic").read()
if len(bladelogic) != 0:
    bladelogics=os.popen("ps aux|grep rscd |grep -v grep|awk '{print $1,$2,$8,$11}'").read()
    hostname=subprocess.check_output('hostname',shell=True)
    hostname1="" + hostname.decode().replace('\n',' ') + ""    
    # field names  
    fields = ['Hostname', 'BMC Agent', 'BMC Agent Status' ]
    # data rows of csv file
    rows = [[f""+str(hostname1), f""+str(bladelogic), f""+str(bladelogics) ]] 

    # name of csv file
    filename = "CSV_OUTPUT_NEW_N/Bladelogic.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)
else:
    print("bladelogic package is not installed")

