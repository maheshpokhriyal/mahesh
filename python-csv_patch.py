import os
import subprocess
import os.path
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

#patch=os.popen("dnf updateinfo list --security|grep -Ev  'Low/Sec.|Moderate/Sec.|Updating|metadata|Enterprise'|head -20").read()
#with open("Patch.txt","w") as wh:
#    wh.write(patch)
#wh.close()
col_names = ['Advisories', 'Security', 'Security-Patches']
data = pd.read_csv(r'Patch.txt', sep=' ', names=col_names, index_col=0, header=None)
data.to_csv('Patch1.csv')

df = pd.read_csv("Patch1.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/PATCH.csv", index=False)
