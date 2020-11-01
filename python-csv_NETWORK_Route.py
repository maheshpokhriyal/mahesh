import os
import subprocess
import os.path
import csv
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

networkr=os.popen("/usr/sbin/route -n|grep -Ev 'Kernel|Destination'|awk '{print $1,$2,$3,$4,$5,$6,$7,$8}'").read()
with open("NETWORK_Route.txt","w") as wh:
    wh.write(networkr)
wh.close()
col_names = ['Destination', 'Gateway', 'Genmask', 'Flags', 'Metric', 'Ref', 'Use', 'Iface']
data = pd.read_csv(r'NETWORK_Route.txt', sep=' ', names=col_names, index_col=0, header=None)
data.to_csv('Route.csv')

df = pd.read_csv("Route.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/NETWORK_Route.csv", index=False)
