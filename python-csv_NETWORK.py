import os
import subprocess
import os.path
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

nw=os.popen("ip -o -4 addr list |awk '{print $2,$4,$6}'|grep -v lo").read()
with open("NETWORK.txt","w") as wh:
    wh.write(nw)
wh.close()
col_names = ['Interface Device', 'IP Address', 'Broadcast IP']
data = pd.read_csv(r'NETWORK.txt', sep=' ', names=col_names, index_col=0, header=None)
data.to_csv('NETWORK1.csv')

df = pd.read_csv("NETWORK1.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/NETWORK.csv", index=False)
