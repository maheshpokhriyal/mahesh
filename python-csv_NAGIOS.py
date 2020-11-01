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

nacl=os.popen("rpm -qa atos-cmf-client-nacl").read()
if len(nacl) != 0:
    nacls=os.popen("su - nagios -c 'NaCl/NaCl -s 192.168.1.10'").read()
    ase = os.popen("rpm -q ase").read()
    ase_service=os.popen("systemctl is-active ase").read()
    # field names  
    fields = ['Hostname', 'CMF Nagios Agent', 'CMF Nagios Agent Status', 'ASE Agent', 'ASE Agent Status' ]
    # data rows of csv file
    rows = [[(f""+str(hostname1)), (f""+str(nacl)), (f""+str(nacls)), (f""+str(ase)), (f""+str(ase_service))]] 

    # name of csv file
    filename = "CSV_OUTPUT_NEW_N/NAGIOS.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        csvwriter.writerows(rows)
else:
    print("atos-cmf-client-nacl package is not installed")

