
import subprocess
import netifaces
from functools import reduce
from numpy.core import long
ip2int = lambda ip: reduce(lambda a,b: long(a)*256 + long(b), ip.split('.'))
int2ip = lambda num: '.'.join( [ str((num >> 8*i) % 256)  for i in [3,2,1,0] ])
# print(netifaces.interfaces())
addrs = netifaces.ifaddresses('wlp2s0')

ip = addrs[netifaces.AF_INET][0]['addr']
mask = addrs[netifaces.AF_INET][0]["netmask"]
def available(ip):
    ret = subprocess.Popen(['fping', '-a','-c','1',ip],stderr=subprocess.PIPE)
    ret.wait()
    if ret.returncode == 0:
        return True
    return False

mask_int = ip2int(mask)
ip_int = ip2int(ip)
zeroslots = mask_int ^ 0b11111111111111111111111111111111

startIP_int = ip_int & mask_int
startIP = int2ip(startIP_int)
endIP_int = startIP_int ^ zeroslots
endIP = int2ip(endIP_int)
print(startIP)
print(endIP)
# print(ip_int)
# print(mask_int)
# print("{0:b}".format(zeroslots))
# print("{0:b}".format(mask_int))
# print("{0:b}".format(ip_int))
# print("{0:b}".format(startIP_int))
iparr = []
for i in range(startIP_int+1, endIP_int):
    ip = int2ip(i)
    iparr.append(ip)
print(iparr)

#     for ip, proc in p.items():
#         if proc.poll() is not None: # ping finished
#             del p[ip] # remove from the process list
#             if proc.returncode == 0:
#                 print('%s active' % ip)
#             elif proc.returncode == 1:
#                 print('%s no response' % ip)
#             else:
#                 print('%s error' % ip)
#             break

# print(mask)
# print(ip)
#

