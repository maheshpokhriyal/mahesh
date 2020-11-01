import os
import subprocess
import os.path
import csv
import pandas as pd

os.system("/usr/bin/python3 tss-script-new_N.py")
col_names = ['Hostname', 'Measure ID', 'Measure Title','TSS Recommendation','Current Value','Compliance/Non-Compliance']
data = pd.read_csv('TSS.txt', sep = ':', names=col_names, index_col=0, header=None)
data.to_csv('CSV_OUTPUT_NEW_N/Atos_TSS.csv')
