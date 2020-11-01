import os
import subprocess
import os.path
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

fs=os.popen("df -TPh|grep -Ev 'Filesystem|devtmpfs|tmpfs'|awk '{print $1,$2,$3,$4,$5,$6,$7}'").read()
with open("DISK.txt","w") as wh:
    wh.write(fs)
wh.close()
col_names = ['Filesystem', 'FilesystemType', 'Size', 'Used', 'Avail', 'Use%', 'MountedOn']
data = pd.read_csv(r'DISK.txt', sep=' ', names=col_names, index_col=0, header=None)
data.to_csv('DISK.csv')

df = pd.read_csv("DISK.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/DISK_INFO.csv", index=False)
