#!/usr/bin/python
import os
import subprocess
from multiprocessing.pool import ThreadPool

SUBNET="192.168.101."
START_HOST=10
END_HOST=11
PROCS=20
HOST_ARR = []
NMAP_ARR = []
RES_ARR = []
QUIET_ARR = [] 
    
def ping_host(host):
    # ping -c 1 10.11.1.5 | grep "64 bytes from " | awk '{print $4}' | cut -d":" -f1 
    p_result = os.system("ping -c1 -W1 %s > /dev/null" % host)
    if p_result == 0:
        RES_ARR.append("%s" % host)
    else:
        NMAP_ARR.append(host)
    

def nmap_host(host):
    cmd = "nmap %s -n -sP | grep report | cut -d\" \" -f5" % host
    n_result = subprocess.check_output(cmd, shell=True)
    rLen = len(n_result)
    if rLen > 1:
        #strip method due to newline at end of response.
        QUIET_ARR.append("%s".strip() % host)
        

def sort_ip_list(ip_list):
    """Sort an IP address list."""
    from IPy import IP
    ipl = [(IP(ip).int(), ip) for ip in ip_list]
    ipl.sort()
    return [ip[1] for ip in ipl]
    
# Change the nmap Args here for more details
# ie sS sT -V -A etc etc
# this will obviously increase processing time.
def scan_host(host):
    cmd = "nmap -Pn %s" % host
    sc_res = subprocess.check_output(cmd, shell=True)
    sLen = len(sc_res)
    if sLen > 1:
        fname="host_%s_nmap.txt" % str(host)
        target_host=open(fname,'w')
        target_host.write(sc_res)
        target_host.close()
    
    print "Scan results stored: host_%s_nmap.txt" % str(host)
        

p_pool = ThreadPool(processes=PROCS)
n_pool = ThreadPool(processes=PROCS)

for i in range(START_HOST, END_HOST):
    #ping the host
    host = ''.join(SUBNET + str(i))
    HOST_ARR.append(host)


print "Checking ICMP HOST Responses"
p_pool.map(ping_host, HOST_ARR)


print "Checking Down Hosts Against NMAP..."
n_pool.map(nmap_host, NMAP_ARR)



#clear the unfiltered lists
HOST_ARR = []
NMAP_ARR = []

#sort results
RES_ARR = sort_ip_list(RES_ARR)
QUIET_ARR=sort_ip_list(QUIET_ARR)

print "PRINTING Out Responder Results:\n"
for res in RES_ARR:
    print "[+] %s is up" % res
    

print "\nPRINTING Out Hidden Host Results:\n"
for qres in QUIET_ARR:
    print "[+] %s is potentially up and may have been rejecting icmp" % qres



print
print "{} Hosts Responded to Ping".format(len(RES_ARR))
print "{} Hosts Are Potentially Hidden/Not responding to Ping".format(len(QUIET_ARR))

i = int(len(RES_ARR)) + int(len(QUIET_ARR))

print "Total Hosts Responding: %s" % str(i)
print

hosts_arr = RES_ARR + QUIET_ARR


print "############ Starting Full NMAP Scan for %s Hosts ############" % str(i)
print "############ This Will take some time....... Go get a life in mean time ############"
for host in hosts_arr:
    print "Conducting Full scan of Host: %s" % str(host)
    scan_host(host)

