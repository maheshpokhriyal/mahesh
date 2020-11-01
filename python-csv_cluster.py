#!/usr/bin/python3
import os
import os.path
import csv
import subprocess

import pathlib
file = pathlib.Path("/etc/corosync/corosync.conf")
if file.exists ():
    hostname=subprocess.check_output('hostname',shell=True)
    hostname1="" + hostname.decode().replace('\n',' ') + "" 
    #cluster=os.popen("pcs cluster status").read().splitlines()
    #with open("pcs.txt","w") as wh:
    #    wh.write(cluster)
    #wh.close()
    cluster=os.popen("cat pcs.txt|grep -Ev 'Cluster Status'").read()

    # field names  
    fields = ['Hostname', 'Cluster Status']
    # data rows of csv file
    rows = [[f""+str(hostname1), f""+str(cluster)]]

    # name of csv file
    filename = "CSV_OUTPUT_NEW_N/Redhat_Cluster.csv"

    # writing to csv file
    with open(filename, 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(fields)

        # writing the data rows
        #for row in csvwriter:
        csvwriter.writerows(rows)
else:
    print("Cluster is not Configured")
