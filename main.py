import subprocess
import netifaces

# print(netifaces.interfaces())
addrs = netifaces.ifaddresses('wlp2s0')
print(addrs[netifaces.AF_INET][0]["netmask"])
