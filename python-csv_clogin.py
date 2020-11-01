import os
import subprocess
import os.path
import pandas as pd
import csv

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

login=os.popen("/usr/bin/who|grep -Ev tty|awk '{print $1,$2,$3,$4,$5}'").read()
with open("clogin.txt","w") as wh:
    wh.write(login)
wh.close()
col_names = ['Login', 'Terminal', 'Login-Date', 'Login-Time', 'Remote-Server']
data = pd.read_csv(r'clogin.txt', sep=' ', names=col_names, index_col=0, header=None)
data.to_csv('clogin.csv')

df = pd.read_csv("clogin.csv")
df.insert(0, column = "Hostname", value = hostname1)
df.head()
df.to_csv("CSV_OUTPUT_NEW_N/Current_User_Login.csv", index=False)
