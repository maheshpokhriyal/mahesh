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

rn=subprocess.check_output('systemctl get-default',shell=True)
rn1=""+ rn.decode().replace('\n','') +""

# field names  
fields = ['Hostname', 'RUNLEVEL']
# data rows of csv file
rows = [[f""+str(hostname1), f""+str(rn1)]]

# name of csv file
filename = "CSV_OUTPUT_NEW_N/RUNLEVEL.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
