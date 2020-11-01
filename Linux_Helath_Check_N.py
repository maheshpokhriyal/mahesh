#!/usr/bin/python3
try:
    #from tabulate import tabulate
    import tabulate
    import psutil
    import subprocess
    from tabulate import tabulate
except ModuleNotFoundError as err:
    # Error handling
    print(err)
mntpoints = psutil.disk_partitions()

## Define the Threshold Value ##
def test(per):
    if per < 90:
        th1='OK'

    elif (per >= 90 and per < 95):
        th1="WARNING"

    elif per >= 95:
        th1="CRITICAL"
    return th1

fs=[]
for mnt in mntpoints:
    hostname=subprocess.check_output('hostname',shell=True)
    hostname1="" + hostname.decode().replace('\n',' ') + ""
    used=psutil.disk_usage(mnt.mountpoint).percent
    ab=[""+str(hostname1)+"",mnt.mountpoint,used,test(used)]
    fs.append(ab)

## Define Define the Threshold Value for CPU ##
cpu=100 - psutil.cpu_percent()
def testc(per):
    if per < 90:
        th1='OK'

    elif (per >= 90 and per < 100):
        th1="WARNING"

    elif per >= 100:
        th1="CRITICAL"
    return th1

tcpu=testc(cpu)

## Define Define the Threshold Value for Memory and Virtual Memory ##
mem=psutil.virtual_memory().percent
swap=psutil.swap_memory().percent

def test(per):
    if per < 80:
        th1='OK'

    elif (per >= 80 and per < 99):
        th1="WARNING"

    elif per >= 99:
        th1="CRITICAL"
    return th1

    return th1
tmem=test(mem)
tswap=test(swap)
fs.append([""+str(hostname1)+"", 'CPU', cpu, tcpu])
fs.append([""+str(hostname1)+"", 'MEMORY',  mem, tmem])
fs.append([""+str(hostname1)+"", 'SWAP', swap, tswap])

table=tabulate(fs,headers=[],tablefmt='plain')
with open('HEALTH.txt', 'w') as f:
	f.write(table)
f.close()
