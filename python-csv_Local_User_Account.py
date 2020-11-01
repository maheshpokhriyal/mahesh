import os
import subprocess
import os.path
import csv
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

users=os.popen("cat /etc/passwd|grep '^root'|awk -F: '{print $1,$3,$4,$6,$7}';awk -F: '$3 >=1000 {print $1,$3,$4,$6,$7}' /etc/passwd|grep -Ev nobody").read()
with open("user.txt","w") as wh:
    wh.write(users)
wh.close()
col_names = ['UserName', 'UID', 'GID', 'HomeDirectory', 'DefaultShell']
data = pd.read_csv(r'user.txt', sep=' ', names=col_names, index_col=0, header=None)
data.to_csv('user.csv')

df = pd.read_csv("user.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/Local_User_Account.csv", index=False)
