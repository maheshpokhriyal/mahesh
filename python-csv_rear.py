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

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

rear = os.popen("rpm -qa rear").read()
if len(rear) != 0:
    rears=os.popen("/usr/sbin/rear -V").read()
    
    # field names  
    fields = ['Hostname', 'Rear', 'Rear Service' ]
    # data rows of csv file
    rows = [[f""+str(hostname1), f""+str(rear), f""+str(rears) ]] 

    # name of csv file
    filename = "CSV_OUTPUT_NEW_N/System_Recovery_Tool.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)
else:
    print("rear package is not installed")
