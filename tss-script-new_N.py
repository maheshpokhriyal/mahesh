#!/usr/bin/python3
try:
    import subprocess
    import os
    import os.path
    from os import path
    from pathlib import Path
    from subprocess import Popen, PIPE
except ModuleNotFoundError as err:
    # Error handling
    print(err)

#print("SU00001   Password Maximum Age")

TSS="TSS.txt"

fo=open(TSS,"w")

new_record = ""
fo.write(new_record)

hostname=subprocess.check_output('hostname',shell=True)
hostname1="" + hostname.decode().replace('\n',' ') + ""

## Verify Password Maximum Age ##
max=int(subprocess.check_output('grep "^PASS_MAX_DAYS" /etc/login.defs |awk \'{print $2}\'',shell=True))
if max == 90:
    new_record = ""+ str(hostname1) +":SU00001:Password Maximum Age:90: " + str(max) + ":Compliance\n" 
else:
    new_record = ""+ str(hostname1) +":SU00001:Password Maximum Age:90: " + str(max) + ":Non-Compliance\n" 
fo.write(new_record)

## Verify password fields are empty OR Not ##
#print("SU00004   Ensure password fields are not empty")
empty=subprocess.check_output('awk -F: \'($2 == \"\" ) { print $1 \" does not have a password \"}\' /etc/shadow',shell=True)
if empty == b'':
    new_record = ""+ str(hostname1) +":SU00004:Ensure password fields are not empty:Password field should not be Empty:verify that no output is returned=>"+  empty.decode().replace('\n','') + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00004:Ensure password fields are not empty:Password field should not be Empty:verify that no output is returned=>"+  empty.decode().replace('\n','') + ":Non-Compliance\n"
fo.write(new_record)

## Verify passwords complexity ##
#print("SU00005   All passwords must match a certain level of complexity")
cmd_result=subprocess.check_output('grep ^minclass /etc/security/pwquality.conf | awk \'{print $3}\'',shell=True)
if cmd_result == b'':
    minclass = 0
else:
    minclass = int(cmd_result) 
if minclass == 4: 
    new_record= ""+ str(hostname1) +":SU00005:Password Complexity:4:" + str(minclass) + ":Compliance\n"
else:
    new_record= ""+ str(hostname1) +":SU00005:Password Complexity:4::Non-Compliance\n"
fo.write(new_record)

## Verify Password Remember field ##
#print("SU00006 Ensure password reuse is limited")
cmd_result=subprocess.check_output('grep -E \'^\s*password\s+(requisite|sufficient)\s+(pam_pwquality\.so|pam_unix\.so)\s+.*remember=([5-9]|[1-4][0-9])[0-9]*\s*.*$\' /etc/pam.d/system-auth|awk -F= \'{print $2}\'',shell=True)
if cmd_result == b'':
    remember = 0
else:
    remember = int(cmd_result)
if remember >= 5:
    new_record = ""+ str(hostname1) +":SU00006:Password History:5:" + str(remember) + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00006:Password History:5::Non-Compliance\n"
fo.write(new_record)

## Verify Password length ##
#print("SU00007 All passwords of all users must have a minimum length of 15 characters")
cmd_result=subprocess.check_output('grep ^minlen /etc/security/pwquality.conf | awk \' { print $3 }\'',shell=True)
if cmd_result == b'': 
    minlen = 0
else:
    minlen = int(cmd_result)
if minlen >= 15:
    new_record = ""+ str(hostname1) +":SU00007:Password Length:15:" + str(minlen) + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00007:Password Length:15::Non-Compliance\n"
fo.write(new_record)

## Verify auth events from rsyslog.conf file ##
#print("SU00008   Enable auth and info logging subsystem to log all auth events")
log=subprocess.check_output('egrep \'^auth*|info\' /etc/rsyslog.conf|awk \'{print $1}\'|grep -Ev \'#\'',shell=True)
if log == "^info|^auth":
    new_record=""+ str(hostname1) +":SU00008:Enable auth and info logging:*.info;mail.none;authpriv.none;cron.none:" + log.decode().replace('\n',' ') + ":Compliance\n"
else:
    new_record=""+ str(hostname1) +":SU00008:Enable auth and info logging:*.info;mail.none;authpriv.none;cron.none:" + log.decode().replace('\n',' ') + ":Non-Compliance\n"
fo.write(new_record)

## Verify Ownership and Permissions of files ##
#print("SU00009 Monitor System Files for Ownership and Permissions")
path = Path("/boot/grub2/grub.cfg")
owner = path.owner()
w=(f"{owner}")
#print(w)
if w == "root":
    new_record = f""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure root is owner of " +str(path)+" file: " +str(path)+"=>" +str(owner)+":Compliance\n"
else:
    new_record = f""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure root is owner of " +str(path)+" file:" +str(path)+" =>" +str(owner)+":Non Compliance\n"
fo.write(new_record)

fname = "/boot/grub2/grub.cfg"
cmd = "stat -c '%A %a %n' " + fname
out = Popen(cmd, shell=True, stdout=PIPE).communicate()[0].split()[1].decode()
if out == "600":
    new_record = ""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure permission is 600 of  " + fname + " file: " + fname + " => "+ str(out) +" :Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure permission is 600 of " + fname + " file: " + fname + " => "+ str(out) +" :Non Compliance\n"
fo.write(new_record)

path1 = Path("/etc/pam.d")
owner1 = path1.owner()
group1 = path1.group()
w1=(f"{owner1};{group1}")
if w1 == "root;root":
    new_record = f""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure root is owner & Group of " +str(path1)+" directory: " +str(path1)+"="+str(w1)+":Compliance\n"
else:
    new_record = f""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure root is owner & Group of " +str(path1)+" directory: " +str(path1)+"=" +str(w1)+":Non Compliance\n"
fo.write(new_record)

fname1 = "/etc/pam.d"
cmd1 = "stat -c '%A %a %n' " + fname1
out1 = Popen(cmd1, shell=True, stdout=PIPE).communicate()[0].split()[1].decode()
if out1 == "755":
    new_record = ""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure permission is 755 of  " + fname1 + " file: " + fname1 + " => "+ str(out1) +" :Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure permission is 755 of " + fname1 + " file: " + fname1 + " => "+ str(out1) +" :Non Compliance\n"
fo.write(new_record)

path2 = Path("/etc/passwd")
owner2 = path2.owner()
w2=(f"{owner2}")
if w2 == "root":
    new_record = f""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure root is owner of " +str(path2)+" file: " +str(path2)+"=" +str(w2)+":Compliance\n"
else:
    new_record = f""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure root is owner of " +str(path2)+" file: " +str(path2)+"=" +str(w2)+":Non Compliance\n"
fo.write(new_record)

fname2 = '/etc/passwd'
cmd2 = "stat -c '%A %a %n' " + fname2
out2 = Popen(cmd2, shell=True, stdout=PIPE).communicate()[0].split()[1].decode()
if out2 == "644":
    new_record = ""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure permission is 644 of " + fname2 + " file: " + fname2 + " => "+ str(out2) +" :Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure permission is 644 of " + fname2 + " file: " + fname2 + " => "+ str(out2) +" :Non Compliance\n"
fo.write(new_record)

path3 = Path("/etc/shadow")
owner3 = path3.owner()
w3=(f"{owner3}")
if w3 == "root":
    new_record = f""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure root is owner of " +str(path3)+" file: " +str(path3)+"=" +str(w3)+":Compliance\n"
else:
    new_record = f""+ str(hostname1) +":SU00009:Monitor System Files for Ownership and Permissions:Ensure root is owner of " +str(path3)+" file: " +str(path3)+"=" +str(w3)+":Non Compliance\n"
fo.write(new_record)

## Verify SSH root login is disabled OR Enabled ##
#print("SU00014   Ensure SSH root login is disabled")
cmd_result=subprocess.check_output('sshd -T | grep permitrootlogin|awk \'{print $2}\'',shell=True)
if cmd_result == b'yes\n':
    login = 'yes'
else:
    login = 'no'
if login == 'no':
    new_record=""+ str(hostname1) +":SU000014: Ensure SSH root login:No:" + login + ":Compliance\n"
else:
    new_record=""+ str(hostname1) +":SU000014: Ensure SSH root login:No:" + login + ":Non-Compliance\n"
fo.write(new_record)

## Verify “Rhosts” Functionality is Disabled OR enabled ##
#print("SU00017   SSH “Rhosts” Functionality Disabled")
cmd_result=subprocess.check_output('sshd -T | grep ignorerhosts|awk \'{print $2}\'',shell=True)
if cmd_result == b'yes\n':
    rhosts = 'yes'
else:
    rhosts = 'no'
if rhosts == "yes":
    new_record = ""+ str(hostname1) +":SU000017: SSH 'Rhosts' Functionality Disabled:yes:' + rhosts + ':Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU000017: SSH 'Rhosts' Functionality Disabled:yes:' + rhosts + ':Non-Compliance\n"
fo.write(new_record)

## Veirfy IP forwarding is disabled OR Enabled ##
#print("SU00021   Ensure IP forwarding is disabled")
cmd_result=subprocess.check_output('sysctl net.ipv4.ip_forward|awk -F= \'{print $2}\'',shell=True)
if cmd_result == b' 1\n':
    ipfwd = 1
else:
    ipfwd = 0
if ipfwd == 0:
    new_record=""+ str(hostname1) +":SU00021:Ensure IP forwarding:0:" + str(ipfwd) + ":Compliance\n"
else:
    new_record=""+ str(hostname1) +":SU00021:Ensure IP forwarding:0:" + str(ipfwd) + ":Non-Compliance\n"
fo.write(new_record)

## Verify source routed packets status ##
#print("SU00021 Ensure source routed packets are not accepted")
cmd_result=subprocess.check_output('sysctl net.ipv4.conf.all.accept_source_route|awk -F= \'{print $2}\'',shell=True)
if cmd_result == b' 1\n':
    iproute = 1
else:
    iproute = 0
if iproute == 0:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:accept_source_route(ipv4)=>0:accept_source_route(ipv4) => "+ str(iproute) + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:accept_source_route(ipv4)=>0:accept_source_route(ipv4) => " + str(iproute) + ":Non-Compliance\n"
fo.write(new_record)

cmd_result=subprocess.check_output('sysctl net.ipv6.conf.all.accept_source_route|awk -F= \'{print $2}\'',shell=True)
if cmd_result == b' 1\n':
    iproute1 = 1
else:
    iproute1 = 0
if iproute1 == 0:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:accept_source_route(ipv6)=>0:accept_source_route(ipv6) => "+ str(iproute1) + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:accept_source_route(ipv6)=>0:accept_source_route(ipv6) => " + str(iproute1) + ":Non-Compliance\n"
fo.write(new_record)

cmd_result=subprocess.check_output('sysctl net.ipv4.conf.all.forwarding|awk -F= \'{print $2}\'',shell=True)
if cmd_result == b' 1\n':
    ipfrwd = 1
else:
    ipfrwd = 0
if ipfrwd == 0:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:ALL_Forwarding(ipv4)=>0:ALL_Forwarding(ipv4) => "+ str(ipfrwd) + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:ALL_Forwarding(ipv4)=>0:ALL_Forwarding(ipv4) => " + str(ipfrwd) + ":Non-Compliance\n"
fo.write(new_record)

cmd_result=subprocess.check_output('sysctl net.ipv6.conf.all.forwarding|awk -F= \'{print $2}\'',shell=True)
if cmd_result == b' 1\n':
    ipfrwd1 = 1
else:
    ipfrwd1 = 0
if ipfrwd1 == 0:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:ALL_Forwarding(ipv6)=>0:ALL_Forwarding(ipv6) => "+ str(ipfrwd1) + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:ALL_Forwarding(ipv6)=>0:ALL_Forwarding(ipv6) => " + str(ipfrwd1) + ":Non-Compliance\n"
fo.write(new_record)

cmd_result=subprocess.check_output('sysctl net.ipv4.conf.all.accept_redirects|awk -F= \'{print $2}\'',shell=True)
if cmd_result == b' 1\n':
    ipredct = 1
else:
    ipredct = 0
if ipredct == 0:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:All accept_redirects(ipv4)=>0:All accept_redirects(ipv4) => "+ str(ipredct) + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:All accept_redirects(ipv4)=>0:All accept_redirects(ipv4) => " + str(ipredct) + ":Non-Compliance\n"
fo.write(new_record)

cmd_result=subprocess.check_output('sysctl net.ipv6.conf.all.accept_redirects|awk -F= \'{print $2}\'',shell=True)
if cmd_result == b' 1\n':
    ipredct1 = 1
else:
    ipredct1 = 0
if ipredct1 == 0:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:All accept_redirects(ipv6)=>0:All accept_redirects(ipv6) => " + str(ipredct1) + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:All accept_redirects(ipv6)=>0:All accept_redirects(ipv6) => " + str(ipredct1) + ":Non-Compliance\n"
fo.write(new_record)

cmd_result=subprocess.check_output('sysctl net.ipv4.conf.all.secure_redirects|awk -F= \'{print $2}\'',shell=True)
if cmd_result == b' 1\n':
    ipsecure = 1
else:
    ipsecure = 0
if ipsecure == 0:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:All secure_redirects(ipv4)=>0:All secure_redirects(ipv4) => " + str(ipsecure) + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:All secure_redirects(ipv4)=>0:All secure_redirects(ipv4) => " + str(ipsecure) + ":Non-Compliance\n"
fo.write(new_record)

cmd_result=subprocess.check_output('sysctl net.ipv4.conf.all.send_redirects|awk -F= \'{print $2}\'',shell=True)
if cmd_result == b' 1\n':
    ipsend = 1
else:
    ipsend = 0
if ipsend == 0:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:All send_redirects(ipv4)=>0:All send_redirects(ipv4)=>" + str(ipsend) + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00021:Ensure source routed packets are not accepted:All send_redirects(ipv4)=>0:All send_redirects(ipv4)=>" + str(ipsend) + ":Non-Compliance\n"
fo.write(new_record)

## Verify System Logs Retention ##
#print("SU00022 Log Data Retention System Logs (syslog/rsyslog)")
rotate=subprocess.check_output('grep rotate /etc/logrotate.conf|grep -E -v \'log|#\'|awk \'{print $2}\'',shell=True)
if  rotate == b'30\n':
    new_record = ""+ str(hostname1) +":SU00022:Log Data Retention System Logs:rotate=>30:rotate=>"+ rotate.decode().replace('\n','') +":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00022:Log Data Retention System Logs:rotate=>30:rotate=>"+ rotate.decode().replace('\n','') +":Non Compliance\n"
fo.write(new_record)

## Verify Crontab file ownership ##
#print("SU00023  Crontab file ownership")
path4 = Path("/etc/crontab")
owner4 = path4.owner()
w4=(f"{owner4}")
if w4 == "root":
    new_record = f""+ str(hostname1) +":SU00023: Crontab file ownership:Ensure root is owner of {path4} file: {path4}={w4}:Compliance\n"
else:
    new_record = f""+ str(hostname1) +":SU00023: Crontab file ownership:Ensure root is owner of {path4} file: {path4}={w4}:Non Compliance\n"
fo.write(new_record)

fname3 = "/etc/crontab"
cmd3 = "stat -c '%A %a %n' " + fname3
out3 = Popen(cmd3, shell=True, stdout=PIPE).communicate()[0].split()[1].decode()
if out3 == "600":
    new_record = ""+ str(hostname1) +":SU00023:Crontab file ownership:Ensure permission is 600 of " + fname3 + " file: " + fname3 + " => "+ str(out3) +" :Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00023:Crontab file ownership:Ensure permission is 600 of " + fname3 + " file: " + fname3 + " => "+ str(out3) +" :Non Compliance\n"
fo.write(new_record)

## Verify permissions of files ##
#print("SU00023  Ensure permissions on /etc/cron.d are configured")
path5 = Path("/etc/cron.d")
owner5 = path5.owner()
group5 = path5.group()
w5=(f"{owner5};{group5}")
if w5 == "root;root":
    new_record = f""+ str(hostname1) +":SU00023: Ensure permissions on /etc/cron.d are configured:Ensure root is owner and group of {path5} file: {path5}={w5}:Compliance\n"
else:
    new_record = f""+ str(hostname1) +":SU00023: Ensure permissions on /etc/cron.d are configured:Ensure root is owner and group of {path5} file: {path5}={w5}:Non Compliance\n"
fo.write(new_record)

fname4 = "/etc/cron.d"
cmd4 = "stat -c '%A %a %n' " + fname4
out4 = Popen(cmd4, shell=True, stdout=PIPE).communicate()[0].split()[1].decode()
if out4 == "700":
    new_record = ""+ str(hostname1) +":SU00023:Ensure permissions on /etc/cron.d are configured:Ensure permission is 700 of " + fname4 + " file: " + fname4 + " => "+ str(out4) +" :Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00023:Crontab file ownership:Ensure permission is 600 of " + fname4 + " file: " + fname4 + " => "+ str(out4) +" :Non Compliance\n"
fo.write(new_record)

## Verify umask value ##
#print("SU00024 Ownership: root umask")
bashrc=subprocess.check_output('grep "umask" /etc/bashrc|grep -E -v \'By default\'|awk \'($2 != 002)\'|awk \'{print $2}\'',shell=True)
profile=subprocess.check_output('grep "umask" /etc/profile|grep -E -v \'By default\'|awk \'($2 != 002)\'|awk \'{print $2}\'',shell=True)
if bashrc == b'022\n':
    new_record = ""+ str(hostname1) +":SU00024:Ownership - root umask:/etc/bashrc=>022:" + bashrc.decode().replace('\n','') + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00024:Ownership - root umask:/etc/bashrc=>022:" + bashrc.decode().replace('\n','') + ":Non-Compliance\n"
fo.write(new_record)
if profile == b'022\n':
    new_record = ""+ str(hostname1) +":SU00024:Ownership - root umask:/etc/profile=>022:" + profile.decode().replace('\n','') + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00024:Ownership - root umask:/etc/profile=>022:" + profile.decode().replace('\n','') + ":Non-Compliance\n"
fo.write(new_record)

## Verify encryption method ##
#print("SU00025 OS password encryption")
passwdauth=subprocess.check_output('grep -E \'^\s*password\s+sufficient\s+pam_unix.so\s+.*sha512\s*.*$\' /etc/pam.d/password-auth|awk \'{print $4}\'',shell=True)
systemauth=subprocess.check_output('grep -E \'^\s*password\s+sufficient\s+pam_unix.so\s+.*sha512\s*.*$\' /etc/pam.d/system-auth|awk \'{print $4}\'',shell=True)
login=subprocess.check_output('grep ENCRYPT_METHOD /etc/login.defs|awk \'{print $2}\'',shell=True)
if passwdauth == b'sha512\n' and systemauth == b'sha512\n' and login == b'SHA512\n':
    new_record=""+ str(hostname1) +":SU00025:OS password encryption:password-auth =>sha512|system-auth =>sha512|login.defs => SHA512:password-auth => " + passwdauth.decode().replace('\n','') + " |system-auth => " + systemauth.decode().replace('\n','') + " |login.defs => " + login.decode().replace('\n','') + ":Compliance\n"
else:
    new_record=""+ str(hostname1) +":SU00025:OS password encryption:password-auth =>sha512|system-auth =>sha512|login.defs => SHA512:password-auth => " + passwdauth.decode().replace('\n','') + " |system-auth => " + systemauth.decode().replace('\n','') + " |login.defs => " + login.decode().replace('\n','') + ":Non-Compliance\n"
fo.write(new_record)

## Verify .rhost authentication is disabled OR enabled ##
#print("SU00034 Ensure .rhost authentication is disabled in PAM")
pamfile1="/usr/lib64/security/pam_rhosts_auth.so"
pamfile2="/usr/lib64/security/pam_rhosts.so"
if os.path.isfile(pamfile1) and os.path.isfile(pamfile2):
    new_record = ""+ str(hostname1) +":SU00034:Ensure .rhost authentication is disabled in PAM:pam_rhosts_auth OR pam_rhosts.so => File exist:" + pamfile1 + " OR " + pamfile2 + " => File not Exist:Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00034:Ensure .rhost authentication is disabled in PAM:pam_rhosts_auth OR pam_rhosts.so => File exist:" + pamfile1 + " OR " + pamfile2 + " => File not Exist:NonCompliance\n"
fo.write(new_record)

## Verify NTP Client is running OR Not ##
#print("SU00035 Ensure NTP Client is running on all Unix Computer")
ntpclient = subprocess.check_output('systemctl is-enabled chronyd | awk \'{ print $1 }\'',shell=True)
if ntpclient == b'enabled\n':
    new_record = ""+ str(hostname1) +":SU00035:Ensure NTP Client is running on all Unix Computer:NTP Client Chronyd => Enabled:NTP Client Chronyd => " + ntpclient.decode().replace('\n','') + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00035:Ensure NTP Client is running on all Unix Computer:NTP Client Chronyd => Enabled:NTP Client Chronyd => " + ntpclient.decode().replace('\n','') + ":Non-Compliance\n"
fo.write(new_record)

## Verify SSH warning banner is configured OR Not ##
#print("SU00039 Ensure SSH warning banner is configured")
banner=subprocess.check_output('sshd -T | grep banner|awk \'{print $2}\'',shell=True)
if banner != b'none\n':
    new_record = ""+ str(hostname1) +":SU00039:Ensure SSH warning banner is configured:Banner => /etc/issue.net:Banner => " + banner.decode().replace('\n','') + ":Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00039:Ensure SSH warning banner is configured:Banner => /etc/issue.net:Banner => " + banner.decode().replace('\n','') + ":Non-Compliance\n"
fo.write(new_record)

## Verify Password faillock is configured OR not ##
#print("SU00041 Ensure lockout for failed password attempts is configured")
pamf=subprocess.check_output('grep -E \'pam_faillock.so\' /etc/pam.d/password-auth /etc/pam.d/system-auth|awk -F" " \'{print $3}\'|uniq',shell=True)
pamt=subprocess.check_output('grep -E \'pam_tally2.so\' /etc/pam.d/password-auth /etc/pam.d/system-auth|awk -F" " \'{print $3}\'|uniq',shell=True)
if pamt == b'pam_tally2.so\n' and pamf == b'pam_faillock.so\n':
    new_record = ""+ str(hostname1) +":SU00041:Ensure lockout for failed password attempts is configured:pam_faillock.so OR pam_tally2.so configured on password-auth & system-auth:" + pamf.decode().replace('\n','') + " OR " + pamt.decode().replace('\n','') + " configured on password-auth & system-auth:Compliance\n"
else:
    new_record = ""+ str(hostname1) +":SU00041:Ensure lockout for failed password attempts is configured:pam_faillock.so OR pam_tally2.so configured on password-auth & system-auth:" + pamf.decode().replace('\n','') + " OR " + pamt.decode().replace('\n','') + " not configured on password-auth & system-auth:Non-Compliance\n"
fo.write(new_record)

## Verify Duplicate UID ##
#print("SU00042 Duplicate UID")
num_of_uids=int(subprocess.check_output('cut -f3 -d":" /etc/passwd | wc -l',shell=True))
uniq_num_of_uids=int(subprocess.check_output('cut -f3 -d":" /etc/passwd | sort -n | uniq | wc -l',shell=True))
os.system("cat /dev/null > /var/tmp/tss-script-new-uids.tmp")
if num_of_uids == uniq_num_of_uids:
    new_record = ""+ str(hostname1) +":SU00042:Duplicate UID:No Duplicate UID:No Duplicate UID:Compliance\n"
else:
    cmd = '''
    /bin/cat /etc/passwd | cut -f3 -d":" | /bin/sort -n | /usr/bin/uniq -c | while read x
    do
        set - $x
        if [ $1 -gt 1 ]; then
            users=`/bin/gawk -F: '($3 == n) {print $1}' n=$2 /etc/passwd | xargs`
            echo -e "$(hostname):SU00042:Duplicate UID:No Duplicate UID:Duplicate UID ($2)=${users}:Non-Compliance"   >> /var/tmp/tss-script-new-uids.tmp
        fi
    done
    '''
    subprocess.check_output(cmd,shell=True)
    infile = open("/var/tmp/tss-script-new-uids.tmp","r")
    new_record = infile.read()
    infile.close()     
fo.write(new_record)

## Verify Duplicate GID ##
#print("SU00042 Duplicate GID")
num_of_gids=int(subprocess.check_output('cut -f3 -d":" /etc/group | wc -l',shell=True))
uniq_num_of_gids=int(subprocess.check_output('cut -f3 -d":" /etc/group | sort -n | uniq | wc -l',shell=True))
os.system("cat /dev/null > /var/tmp/tss-script-new-gids.tmp")
if num_of_gids == uniq_num_of_gids:
    new_record=""+ str(hostname1) +":SU00042:Duplicate GID:No Duplicate GID:No Duplicate GID:Compliance\n"
else:
    cmd = '''
    /bin/cat /etc/group | cut -f3 -d":" | /bin/sort -n | /usr/bin/uniq -c | while read x
    do
        set - $x
        if [ $1 -gt 1 ]; then
            groups=`/bin/gawk -F: '($3 == n) {print $1}' n=$2 /etc/group | xargs`
            echo -e "$(hostname)::SU00042:Duplicate GID:No Duplicate GID:Duplicate GID ($2)=${groups}:Non-Compliance"                  >> /var/tmp/tss-script-new-gids.tmp
        fi
    done
    '''
    subprocess.check_output(cmd,shell=True)
    infile = open("/var/tmp/tss-script-new-gids.tmp","r")
    new_record = infile.read()
    infile.close()     
fo.write(new_record)

## Verify root PATH Integrity ##
#print("SU00043 Ensure root PATH Integrity")
os.system("cat /dev/null > /var/tmp/tss-script-new-root-path.tmp")
cmd='''
for x in $(echo $PATH | tr ":" " ") ; do
        if [ -d "$x" ] ; then
                ls -ldH "$x" | awk '
                $9 == "." {print "   :","SU00043:Ensure root PATH Integrity:PATH does not contains current working directory (.):PATH contains current working directory (.):Non-Compliance"}
              # $9 != "." {print "   :","SU00043:Ensure root PATH Integrity:PATH does not contains current working directory (.):PATH does not contains current working directory (.):Compliance"}
                $3 != "root" {print "   :","SU00043:","Ensure root PATH Integrity:",$9,"is owned by root:",$9,"is not owned by root:Non-Compliance"}
                $3 == "root" {print "   :","SU00043:","Ensure root PATH Integrity:",$9,"is owned by root:",$9,"is owned by root:Compliance"}
                substr($1,6,1) != "-" {print $9, "is group writable"}
                substr($1,9,1) != "-" {print $9, "is world writable"}'
        else
                #echo "$x is not a directory"
                echo "$(hostname):SU00043:Ensure root PATH Integrity:$x is not a directory:$x is not owned by root:Non-Compliance"
        fi >> /var/tmp/tss-script-new-root-path.tmp
done
'''
subprocess.check_output(cmd,shell=True)
infile = open("/var/tmp/tss-script-new-root-path.tmp","r")
new_record = infile.read()
infile.close()     
fo.write(new_record)
