import os
import subprocess
import os.path
import csv
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

package=os.popen("/bin/rpm -qa|sort|head -20").read()
with open("package.txt","w") as wh:
    wh.write(package)
wh.close()
col_names = ['Package']
data = pd.read_csv(r'package.txt', names=col_names, index_col=0, header=None)
data.to_csv('PACKAGES.csv')

df = pd.read_csv("PACKAGES.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/Installed_PACKAGES.csv", index=False)
