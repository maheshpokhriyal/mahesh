#!/usr/bin/python3
import platform
import os
import subprocess
import sys
import re
import os.path
import csv
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""


ms=os.popen("ls /var/log/messages").read()
if len(ms) != 0:
    m=os.popen('ls -lh /var/log/messages|awk \'{print $9 ";" $6,$7,$8 ";" $5 ";" echo "Live Log File"}\'').read()
else:
    m="/var/log/messages ; File not exist ; ; \n"
ms1=os.popen("ls /var/log/messages-*").read()
if len(ms1) != 0:
    m1=os.popen('ls -lh /var/log/messages-*|awk \'{print $9 ";" $6,$7,$8 ";" $5 ";" echo "Archive Log File"}\'').read()
else:
    m1="Archive Log File not exist ; ; ; \n"
se=os.popen("ls /var/log/secure").read()
if len(se) != 0:
    s=os.popen('ls -lh /var/log/secure|awk \'{print $9 ";" $6,$7,$8 ";" $5 ";" echo "Live Log File"}\'').read()
else:
    s="/var/log/secure ; File not exist ; ; \n"
se1=os.popen("ls /var/log/secure-*").read()
if len(se1) != 0:
    s1=os.popen('ls -lh /var/log/secure-*|awk \'{print $9 ";" $6,$7,$8 ";" $5 ";" echo "Archive Log File"}\'').read()
else:
    s1="Archive Log File not exist ; ; ; \n"
bo=os.popen("ls /var/log/boot.log").read()
if len(bo) != 0:
    b=os.popen('ls -lh /var/log/boot.log|awk \'{print $9 ";" $6,$7,$8 ";" $5 ";" echo "Live Log File"}\'').read()
else:
    b="Archive Log File not exist ; ; ; \n"
bo1=os.popen("ls /var/log/boot.log-*").read()
if len(bo1) != 0:
    b1=os.popen('ls -lh /var/log/boot.log-*|awk \'{print $9 ";" $6,$7,$8 ";" $5 ";" echo "Archive Log File"}\'').read()
else:
    b1="Archive Log File not exist ; ; ; \n"
with open("LOG.txt","w") as wh:
    wh.write(m+s+b+m1+s1+b1)
wh.close()

col_names = ['Log_File', 'Date', 'Size', 'File Type']
data = pd.read_csv(r'LOG.txt', sep=';', names=col_names, index_col=0, header=None)
data.to_csv('Log.csv')

df = pd.read_csv("Log.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/System_Log.csv", index=False)
