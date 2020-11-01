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

tz=subprocess.check_output('timedatectl|grep "Time zone"|awk -F: \'{print $2}\'',shell=True)
tz1=""+ tz.decode().replace('\n','') +""

# field names  
fields = ['Hostname','Time Zone']
# data rows of csv file
rows = [[f""+str(hostname1), f""+str(tz1)]]

# name of csv file
filename = "CSV_OUTPUT_NEW_N/TimeZone.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
