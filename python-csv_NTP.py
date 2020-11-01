import os
import subprocess
import os.path
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""


ch=os.popen("chronyc tracking|grep -Ev 'UTC'").read()
with open("ntp.txt","w") as wh:
    wh.write(ch)
wh.close()
col_names = ['Name', 'Tracking']
data = pd.read_csv(r'ntp.txt', sep = ':', names=col_names, index_col=0, header=None)
data.to_csv('NTP1.csv')

df = pd.read_csv("NTP1.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/NTP.csv", index=False)
