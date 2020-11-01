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
from datetime import date

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

firewalls=os.popen("firewall-cmd --state|grep -v '^$'").read().splitlines()
for line in firewalls:
    fw=line.strip()

fd=os.popen("firewall-cmd --zone=public --list-all").read()

# field names  
fields = ['Hostname', 'Firewall Status', 'Firewalld Configuration' ]
# data rows of csv file
rows = [[f""+str(hostname1), f""+str(fw), f""+str(fd)]] 

# name of csv file
filename = "CSV_OUTPUT_NEW_N/FIREWALL.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
