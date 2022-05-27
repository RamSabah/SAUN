import psutil
import socket

lc = psutil.net_connections('inet')
for c in lc:
    if c.laddr[1] == 3030:
        print(c.pid)
        print(c.laddr[0])



