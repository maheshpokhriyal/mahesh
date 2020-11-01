import os
import subprocess
import os.path
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

process=os.popen("/usr/bin/ps -eo user,pid,cmd|tail -50|grep -Ev 'tail|/usr/bin/ps|awk|sh'|awk '{print $1,$2,$3}'").read()
with open("process.txt","w") as wh:
    wh.write(process)
wh.close()
col_names = ['USER', 'PID', 'CMD']
data = pd.read_csv(r'process.txt', sep=' ', names=col_names, index_col=0, header=None)
data.to_csv('PROCESS.csv')

df = pd.read_csv("PROCESS.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/Running_PROCESS.csv", index=False)
