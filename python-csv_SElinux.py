#!/usr/bin/python3
import platform
import os
import subprocess
import sys
import re
import os.path
import csv
from datetime import date

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

selinux=os.popen("sestatus|grep 'SELinux status'|awk -F: '{print $2}'").read()
se=""+str(selinux)+""

# field names  
fields = ['Hostname', 'SELinux Status']
# data rows of csv file
rows = [[f""+str(hostname1), f""+str(se)]]

# name of csv file
filename = "CSV_OUTPUT_NEW_N/SELINUX.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
