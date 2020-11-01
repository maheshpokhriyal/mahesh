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

networker=os.popen("rpm -qa |grep -i lgto").read()
if len(networker) != 0:
    nwservice=os.popen("systemctl is-active networker").read()
    
    # field names  
    fields = ['Hostname', 'NetWorker Client', 'NetWorker Service' ]
    # data rows of csv file
    rows = [[f""+str(hostname1), f""+str(networker), f""+str(nwservice) ]] 

    # name of csv file
    filename = "CSV_OUTPUT_NEW_N/Backup_Tool_EMC.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)
else:
    print("networker package is not installed")
