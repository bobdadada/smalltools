# -*- coding: utf-8 -*-

import argparse
from socket import *
from threading import *
import nmap

def nmapScan(tgtHost, tgtPort):
    nmScan = nmap.PortScanner()
    nmScan.scan(tgtHost, tgtPort)
    state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
    print("[*] " + tgtHost + " tcp/" + tgtPort + " " + state)

def __main__():
    parser = argparse.ArgumentParser(description="Scan and connect " +\
                                     "the port of target host")
    parser.add_argument(dest='tgtHosts', help='specify target host[s]')    
    parser.add_argument(dest='tgtPort', help='specify target port')
    args = parser.parse_args()
    tgtHosts = args.tgtHosts
    tgtPort = args.tgtPort
    tgtHosts = ['.'.join(tgtHosts.split('.')[0:-1]+ [str(id)]) for id in range(1, 256)]
    if (tgtHosts[0] == None) or (tgtPort == None):
        print('[-] You must specify a target host and port[s].')
        exit(0)
    for tgtHost in tgtHosts:
        t = Thread(target=nmapScan, args=(tgtHost, tgtPort))
        t.start()

if __name__ == '__main__':
    __main__()
