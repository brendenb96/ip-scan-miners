#!/usr/bin/env python

import sys
import requests
from requests.auth import HTTPDigestAuth

IP_START = "192.168.0.1"
IP_END = "192.168.0.254"
USERNAME = "admin"
PASSWORD = "admin"
TIMEOUT= 1.0

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

                miner_config_page = session.get(config_page, timeout=TIMEOUT, auth=HTTPDigestAuth(username,password))
                miner_config_content = miner_config_page.json()
            except Exception as err:
                error_webpage = True

            if error_webpage:
                print "No miner on IP: %s" %ip_dest

            else:
                ip = ip_dest
                pool_one = miner_config_content['pools'][0]['url']
                pool_two = miner_config_content['pools'][1]['url']
                pool_three = miner_config_content['pools'][2]['url']
                hash_rate = miner_status_content['summary']['ghsav']
                type = miner_system_content['minertype']
                name = miner_system_content['hostname']
                uptime = miner_system_content['uptime']
                chain1_temp = miner_status_content['devs'][0]['freq'].split(',')[9].split('=')[1]
                chain2_temp = miner_status_content['devs'][0]['freq'].split(',')[10].split('=')[1]
                chain3_temp = miner_status_content['devs'][0]['freq'].split(',')[11].split('=')[1]
                asic1 = miner_status_content['devs'][0]['chain_acs']
                asic2= miner_status_content['devs'][1]['chain_acs']
                asic3 = miner_status_content['devs'][2]['chain_acs']

                if pool_one.rstrip() == '':
                    pool_one = 'NONE'
                if pool_two.rstrip() == '':
                    pool_two = 'NONE'
                if pool_three.rstrip() == '':
                    pool_three = 'NONE'

                print "#########################"
                print ip
                print pool_one
                print pool_two
                print pool_three
                print hash_rate
                print type
                print name
                print chain1_temp
                print chain2_temp
                print chain3_temp
                print uptime
                print "#########################"

        return 0

    except KeyboardInterrupt:
        print "\nCancelling..."


#############################
if __name__ == "__main__":
    sys.exit(main())
#############################
