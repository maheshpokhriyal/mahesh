import os
import subprocess
import os.path
import csv
import pandas as pd

os.system("/usr/bin/python3 risk-ana-script-new_N.py")
col_names = ['Hostname', 'Risk Measure', 'Risk Assessment','Assessment Result','Risk Severity']
data = pd.read_csv('RISK_ANA.txt', sep = ':', names=col_names, index_col=0, header=None)
data.to_csv('CSV_OUTPUT_NEW_N/Risk_Analysis.csv')
