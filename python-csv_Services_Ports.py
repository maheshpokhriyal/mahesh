import os
import subprocess
import os.path
import csv
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

servicesp=os.popen("netstat -tulp|grep -Ev Active|grep LISTEN|awk '{print $1,$2,$3,$4,$5,$6,$7}'").read()
with open("servicesp.txt","w") as wh:
    wh.write(servicesp)
wh.close()
col_names = ['Proto', 'Recv-Q', 'Send-Q', 'Local-Address', 'Foreign-Address', 'State', 'PID/Program']
data = pd.read_csv(r'servicesp.txt', sep=' ', names=col_names, index_col=0, header=None)
data.to_csv('Servp.csv')

df = pd.read_csv("Servp.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/Services_Ports.csv", index=False)
