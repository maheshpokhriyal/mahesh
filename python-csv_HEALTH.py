import os
import subprocess
import os.path
import csv
import pandas as pd

health=os.popen("/usr/bin/python3 Linux_Helath_Check_N.py").read()
ht=os.popen("cat HEALTH.txt|awk '{print $1,$2,$3,$4}'").read()
with open("HT.txt","w") as wh:
    wh.write(ht)
wh.close()
col_names = ['Hostname', 'Name', 'THRESHOLD(%)', 'STATUS']
data = pd.read_csv(r'HT.txt', sep = ' ', names=col_names, index_col=0, header=None)
data.to_csv('CSV_OUTPUT_NEW_N/HEALTH.csv')
