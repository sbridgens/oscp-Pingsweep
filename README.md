# oscp-Pingsweep

A basic lan pingsweep script created during oscp

1: conducts a basic ping sweep
2: creates a full nmap scan of the online hosts

Item 2 is very slow dependant on the options in the script and the number of hosts.

Example output

```bash
root@kali:~/scripts/python$ python pingsweep.py 
Checking ICMP HOST Responses
Checking Down Hosts Against NMAP...
PRINTING Out Responder Results:

[+] 192.168.101.10 is up

PRINTING Out Hidden Host Results:


1 Hosts Responded to Ping
0 Hosts Are Potentially Hidden/Not responding to Ping
Total Hosts Responding: 1

############ Starting Full NMAP Scan for 1 Hosts ############
############ This Will take some time....... Go get a life in mean time ############
Conducting Full scan of Host: 192.168.101.10
Scan results stored: host_192.168.101.10_nmap.txt



root@kali:~/scripts/python$ cat host_192.168.101.10_nmap.txt

Starting Nmap 7.50 ( https://nmap.org ) at 2017-07-28 05:02 BST
Stats: 0:00:04 elapsed; 0 hosts completed (1 up), 1 undergoing SYN Stealth Scan
SYN Stealth Scan Timing: About 22.35% done; ETC: 05:02 (0:00:17 remaining)
Nmap scan report for 192.168.101.10
Host is up (0.073s latency).
Not shown: 996 filtered ports
PORT     STATE SERVICE
25/tcp   open  smtp
80/tcp   open  http
88/tcp   open  kerberos-sec
8080/tcp open  http-proxy

Nmap done: 1 IP address (1 host up) scanned in 11.18 seconds
```
