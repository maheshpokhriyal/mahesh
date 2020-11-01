import os
import subprocess
import os.path
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

services=os.popen("systemctl list-units --type service|grep -Ev '^$|LOAD|ACTIVE|SUB|loaded units listed|systemctl list-unit-files|jenkins'|awk '{print $1','$2','$3','$4}'").read()
with open("services.txt","w") as wh:
    wh.write(services)
wh.close()
col_names = ['UNIT', 'LOAD', 'ACTIVE', 'SUB']
data = pd.read_csv(r'services.txt', sep=' ', names=col_names, index_col=0, header=None)
data.to_csv('SERVICES.csv')

df = pd.read_csv("SERVICES.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/Running_SERVICES.csv", index=False)
