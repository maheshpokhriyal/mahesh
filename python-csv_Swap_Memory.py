import os
import subprocess
import os.path
import psutil
import csv
import numpy as np
import pandas as pd
from collections import OrderedDict
swap=psutil.swap_memory()

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

tmem = f"{get_size(swap.total)}"
amen = f"{get_size(swap.free)}"
umem = f"{get_size(swap.used)}"
per = f"{swap.percent}%"

fields = ['Hostname', 'Total Memory', 'Available Memory', 'Used Memory', 'Percentage' ]
# data rows of csv file
rows = [[f""+str(hostname1), (f""+str(tmem)), f""+str(amen), f""+str(umem), f""+str(per) ]]

# name of csv file
filename = "CSV_OUTPUT_NEW_N/SWAP_Memory_INFO.csv"

# writing to csv file
with open(filename, 'w') as csvfile:
    # creating a csv writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # writing the data rows
    csvwriter.writerows(rows)
