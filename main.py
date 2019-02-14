import subprocess
import netifaces
import time
from functools import reduce
import requests
from numpy.core import long
from uuid import getnode as get_mac
import argparse

ip2int = lambda ip: reduce(lambda a,b: long(a)*256 + long(b), ip.split('.'))
int2ip = lambda num: '.'.join( [ str((num >> 8*i) % 256)  for i in [3,2,1,0] ])
addrs = netifaces.ifaddresses('wlp2s0')
myip = addrs[netifaces.AF_INET][0]['addr']
print("my IP: "+str(myip))
mask = addrs[netifaces.AF_INET][0]["netmask"]
print("mask:  "+str(mask))
parser = argparse.ArgumentParser(description='Process needed mask')
parser.add_argument('mask', metavar='N', type=str,
                   help='mask ex: 255.255.128.0')
args = parser.parse_args()
# if len(sys.argv) >  0:
#     mask = sys.argv[0]
def available(ip):
    command = ['fping', '-c' ,'1'] +ip
    ret = subprocess.Popen(command,stderr=subprocess.PIPE,
                           stdout=subprocess.PIPE)
    ret.wait()
    output=ret.stdout.read()

    outputstr = output.decode("utf-8")
    # print(outputstr)
    outputstr = outputstr.replace(" ","")
    ips = outputstr.splitlines()
    for ip, a in enumerate(ips):
        pos = a.find(':')
        ips[ip] = a[0:pos]
    return ips
mask_int = ip2int(mask)
ip_int = ip2int(myip)
zeroslots = mask_int ^ 0b11111111111111111111111111111111
startIP_int = ip_int & mask_int
startIP = int2ip(startIP_int)
endIP_int = startIP_int ^ zeroslots
endIP = int2ip(endIP_int)
# print(startIP)
# print(ip_int)
# print(mask_int)
# print("{0:b}".format(zeroslots))
# print("{0:b}".format(mask_int))
# print("{0:b}".format(ip_int))
# print("{0:b}".format(startIP_int))
print('        IP         |         MAC           |          NAME     ')
print('---------------------------------------------------------------')
mac = get_mac()
print(str(myip) + "          " + str(':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2)) ) +  "    Intel Corporate" )
iparr = []
for i in range(startIP_int+1, endIP_int):
    ip = int2ip(i)
    iparr.append(ip)
ips = available(iparr)
for ipw in ips:
    ret = subprocess.Popen(['arp', '-a', ipw], stdout=subprocess.PIPE)
    ret.wait()
    outputarr = []
    output=ret.stdout.read().decode("utf-8")
    outputarr.append(output)
    lines = output.split(" ")
    time.sleep(1)
    macResp = requests.get('https://api.macvendors.com/{}'.format(lines[3]))
    mac = macResp.content.decode(macResp.encoding)

    if not ip_int==ip2int(ipw):
        print(str(ipw) + "          " + lines[3]+"    " + mac )
# print(outputarr)
# print(mask)
# print(ip)
#
# print(endIP)
