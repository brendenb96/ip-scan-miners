#!/usr/bin/env python

import sys
import requests
import json
from requests.auth import HTTPDigestAuth

# THESE NEED TO BE DEFINED DEPENDING ON WHERE THE PROGRAM IS RUN
IP_START = "10.0.0.2"
IP_END = "10.0.0.100"

#LOGIN INFO
USERNAME = "root"
PASSWORD = "root"
TIMEOUT= 2.0

#LIMITS
TEMP_HI_S = 85.0
TEMP_HI_L = 70.0
TEMP_HI_DEF = 85.0

#COLOURS
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = u'\u001b[41m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def ipRange(start_ip, end_ip):
    start = list(map(int, start_ip.split(".")))
    end = list(map(int, end_ip.split(".")))
    temp = start
    ip_range = []
    
    ip_range.append(start_ip)
    while temp != end:
        start[3] += 1
        for i in (3, 2, 1):
            if temp[i] == 256:
                temp[i] = 0
                temp[i-1] += 1
        ip_range.append(".".join(map(str, temp)))    
        
    return ip_range

def main():

    try:
        all_ips = ipRange(IP_START, IP_END)

        for machine in all_ips:
            ip_dest = machine
            username = USERNAME
            password = PASSWORD
            error_webpage = False

            status_page = "http://"+ip_dest+"/cgi-bin/get_miner_status.cgi"
            system_page = "http://"+ip_dest+"/cgi-bin/get_system_info.cgi"
            config_page = "http://"+ip_dest+"/cgi-bin/get_miner_conf.cgi"

            try:
                session = requests.Session()
                miner_status_page = session.get(status_page, timeout=TIMEOUT, auth=HTTPDigestAuth(username,password))
                miner_status_content = miner_status_page.json()

                miner_system_page = session.get(system_page, timeout=TIMEOUT, auth=HTTPDigestAuth(username,password))
                miner_system_content = miner_system_page.json()

                # miner_config_page = session.get(config_page, timeout=TIMEOUT, auth=HTTPDigestAuth(username,password))
                # miner_config_content = miner_config_page.json()
            except Exception as err:
                error_webpage = True

            if error_webpage:
                print WARNING + "No miner on IP: %s" %ip_dest + ENDC

            else:

                print OKBLUE + "########################################################################################################" + ENDC
                print WARNING + "IP: "+ ip_dest + ENDC
                print WARNING + "HOSTNAME: "+miner_system_content['hostname'] + ENDC
                print WARNING + "HASH RATE: "+miner_status_content['summary']['ghsav'] + ENDC
                # print json.dumps(miner_status_content, indent=2)
                for element in miner_status_content['devs']:
                    chain = element['chain_acs']
                    if 'x' in chain:
                        print FAIL + "CHIP STATUS: "+element['chain_acs'] + ENDC
                    else:
                        print OKGREEN + "CHIP STATUS: "+element['chain_acs'] + ENDC

                    temp = float(element['temp'])
                    if 's9' in miner_system_content['hostname'].lower():
                        if temp > TEMP_HI_S:
                            print FAIL + "CHIP TEMP: "+ element['temp'] + ENDC
                        else:
                            print OKGREEN + "CHIP TEMP: " + element['temp'] + ENDC

                    elif 'l3' in miner_system_content['hostname'].lower():
                        if temp > TEMP_HI_L:
                            print FAIL + "CHIP TEMP: "+ element['temp'] + ENDC
                        else:
                            print OKGREEN + "CHIP TEMP: " + element['temp'] + ENDC

                    else:
                        if temp > TEMP_HI_DEF:
                            print FAIL + "CHIP TEMP: "+ element['temp'] + ENDC
                        else:
                            print OKGREEN + "CHIP TEMP: " + element['temp'] + ENDC
                print OKBLUE + "########################################################################################################" + ENDC
                

        return 0

    except KeyboardInterrupt:
        print "\nCancelling..."


#############################
if __name__ == "__main__":
    sys.exit(main())
#############################
