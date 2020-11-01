#!/usr/bin/python3
try:
    import subprocess
    import os
    from pathlib import Path
    from subprocess import Popen, PIPE

except ModuleNotFoundError as err:
    # Error handling
    print(err)

RK="RISK_ANA.txt"
fo=open(RK,"w")

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

new_record = ""
fo.write(new_record)
## Verify "/boot" partition ##
boot=subprocess.check_output('df -Ph|grep /boot |awk \'{print $6}\'',shell=True)
b=""+ boot.decode().replace('\n','') +""
if b == "/boot":
    new_record = ""+ str(hostname1) +":/boot should have separate partition: boot partition =>" + str(b) +":/boot is configured with separate partition:No-Risk\n"
else:
    new_record = ""+ str(hostname1) +":/boot should have separate partition: boot partition =>" + str(b) +":/boot is not configured with separate partition:High-Risk\n"
fo.write(new_record)

## Verify PermitRootLogin value ##
root=subprocess.check_output('grep "^PermitRootLogin" /etc/ssh/sshd_config |awk \'{print $2}\'',shell=True)
r=""+ root.decode().replace('\n','') +""
if r == "yes":
    new_record = ""+ str(hostname1) +":Disable SSH Root Login:PermitRootLogin =>"+ str(r) +":SSH Root Login is Enabled:High-Risk\n"
else:
    new_record = ""+ str(hostname1) +":Disable SSH Root Login:PermitRootLogin =>"+ str(r) +":SSH Root Login is Disable:No-Risk\n"
fo.write(new_record)

## Verify status of "sshd" service ##
s=subprocess.check_output('systemctl is-active sshd',shell=True)
s1=""+ s.decode().replace('\n','') +""
#print(sr)
if s1 == "active":
    new_record = ""+ str(hostname1) +":Enable SSH Service:SSH Service =>"+ str(s1) +": SSH service is running:No-Risk\n"
else:
    new_record = ""+ str(hostname1) +":Enable SSH Service:SSH Service =>"+ str(s1) +": SSH service is not running:High-Risk\n"
fo.write(new_record)

## Verify status of "firewalld" service ##
f=subprocess.check_output('systemctl is-active firewalld||systemctl is-active nftables||systemctl is-active iptables',shell=True)
f1=""+ f.decode().replace('\n','') +""
if f1 == "active":
    new_record = ""+ str(hostname1) +":Enable Firewall Service:Firewall Service =>"+ str(f1) +": Firewall service is running:No-Risk\n"
else:
    new_record = ""+ str(hostname1) +":Enable Firewall Service:Firewall Service =>"+ str(f1) +": Firewall service is not running:High-Risk\n"
fo.write(new_record)

## Verify status of "SELinux" ##
se=subprocess.check_output('sestatus|awk -F: \'{print $2}\'',shell=True)
se1 = se.strip()
se2=""+ se1.decode().replace('\n','') +""
if se2 == "enabled":
    new_record = ""+ str(hostname1) +":Enable SELinux:SELinux =>"+ str(se2) +": SELinux is enabled:No-Risk\n"
else:
    new_record = ""+ str(hostname1) +":Enable SELinux:SELinux =>"+ str(se2) +": SELinux is disabled:MID-Risk\n"
fo.write(new_record)
import pathlib
file = pathlib.Path("/boot/grub2/user.cfg")
if file.exists ():
    gb=subprocess.check_output('grep "^GRUB2_PASSWORD" /boot/grub2/user.cfg |awk -F= \'{print $1}\'',shell=True)
    gb1=""+ gb.decode().replace('\n','') +""
    if gb1 == "GRUB2_PASSWORD":
        new_record = ""+ str(hostname1) +":Enable Grub Password:GRUB2 PASSWORD =>"+ str(gb1) +": Grub Password is enabled:No-Risk\n"
    else:
        new_record = ""+ str(hostname1) +":Enable Grub Password:GRUB2 PASSWORD =>"+ str(gb1) +": Grub Password is disabled:High-Risk\n"
else:
    new_record = "/boot/grub2/grub.cfg => File not exist: "
fo.write(new_record)


## Veify Server sync with NTP OR Not ##
ch=subprocess.check_output('chronyc sources|grep "*"|awk \'{print $1}\'',shell=True)
ch1=""+ ch.decode().replace('\n','') +""
#print(ch1)
if ch1 == "^*":
    new_record = ""+ str(hostname1) +":Enable Time Sync:MS => "+ str(ch1) +": Time sync is enabled:No-Risk\n"
else:
    new_record = ""+ str(hostname1) +":Enable Time Sync:MS => "+ str(ch1) +": Time sync is not enabled:High-Risk\n"
fo.write(new_record)


## Verify Sticky bit permission on "/tmp" ##
st=subprocess.check_output('ls -ld /tmp|awk \'{print $1}\'',shell=True)
st1=""+ st.decode().replace('\n','') +""
if st1 == "drwxrwxrwt.":
    new_record = ""+ str(hostname1) +":Enable sticky bit permission on /tmp:StickyBit => "+ str(st1) +": Sticky Bit is enabled on /tmp:No-Risk\n"
else:
    new_record = ""+ str(hostname1) +":Enable sticky bit permission on /tmp:StickyBit => "+ str(st1) +": Sticky Bit is not enabled on /tmp:High-Risk\n"
fo.write(new_record)

## Verify status of "auditd" Service ## 
au=subprocess.check_output('systemctl is-active auditd.service',shell=True)
au1=""+ au.decode().replace('\n','') +""
if au1 == "active":
    new_record = ""+ str(hostname1) +":Enable auditd service:auditd => "+ str(au1) +": Auditd service is running:No-Risk\n"
else:
    new_record = ""+ str(hostname1) +":Enable auditd service:auditd => "+ str(au1) +": Auditd service is not running:High-Risk\n"
fo.write(new_record)

## Detect all world-writable files ##
wr1=os.popen("find / -xdev -type d \( -perm -0002 -a ! -perm -1000 \)").readlines()
if(len(wr1) == 0):
    new_record = ""+ str(hostname1) +":Detect all world-writable files: " + str(wr1) + ": No Files/Directories are world-writable:No-Risk\n"
else:
    new_record = ""+ str(hostname1) +":Detect all world-writable files: " + str(wr1)  + ": Files/Directories are world-writable:MID-Risk\n"
fo.write(new_record)

## Verify server's default run-level ##
rn=subprocess.check_output('systemctl get-default',shell=True)
rn1=""+ rn.decode().replace('\n','') +""
if rn1 == "multi-user.target":
    new_record = ""+ str(hostname1) +":Enable Multi-user Runlevel:runlevel => "+ str(rn1) +": Server configutred with multi-user.target:No-Risk\n"
else:
    new_record = ""+ str(hostname1) +":Enable Multi-user Runlevel:eunlevel => "+ str(rn1) +": Server configutred with "+ str(rn1) +":MID-Risk\n"
fo.write(new_record)

