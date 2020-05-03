#!/usr/bin/python3

# Import
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from netifaces import AF_INET, AF_INET6, AF_LINK, AF_PACKET, AF_BRIDGE
from threading import Thread
from scapy.all import *
from time import time
from time import sleep
import netifaces as ni
from threadSniffer import Sniffer
import os, sys
import argparse


# Function used to parse input arguments; arguments options:
#   - v : version, default value: '1'
#   - c : community, default value: 'community'
#   - i : ip, default value 'localhost'
def parsingArgs():
    parser = argparse.ArgumentParser(description='Tool used to analize an snmp agent netstat')

    parser.add_argument('-u', metavar='url', type=str, nargs='?', default='http://localhost:9999', dest='db_url',
                        help='influxDB url')

    parser.add_argument('-t', metavar='token', type=str, nargs='?', default='iBkhHJ7Bp_Ekf7e42zFtqPgenZfnbVKnKseAwrxRoy6CuZPu2_667VGTMg2D5HYAJpkK9xM9wpHr6JAx8E-ZDA==', dest='db_token',
                        help='influxDB token')

    parser.add_argument('-o', metavar='organization', type=str, nargs='?', default='m.biscosi', dest='db_org',
                        help='influxDB organization')

    parser.add_argument('-b', metavar='bucket', type=str, nargs='?', default='host_monitoring', dest='db_bucket',
                        help='influxDB bucket')

    args = parser.parse_args()

    return args


# Function that get the local private ip address of all interfaces
def getIP():
    addr_if = []
    addr_ip = []

    print('Interfaces found:')

    for interface in ni.interfaces():
        addr_if.append(interface)
        addr_ip.append(ni.ifaddresses(interface)[AF_INET][0]['addr'])
        print(interface, ': ', ni.ifaddresses(interface)[AF_INET][0]['addr'])

    return addr_if, addr_ip


# Function used to connect to the database
def influxDBConnection(db_url, db_token, db_org):
    try:
        client = InfluxDBClient(url=db_url,
                                token=db_token,
                                org=db_org)

        write_api = client.write_api(write_options=SYNCHRONOUS)
    except:
        print('ERROR: Database unavailable, check if -u, -t and -o options are correct')
        exit(1)

    return client, write_api


# Function used to create Threads that sniff packets, one thread per interface
def sniff_pkt(interface, ipv4, sniffer_list, counter):
    sniffer_list[counter] = Sniffer(interface=interface, ipv4=ipv4)
    sniffer_list[counter].start()


# Application cicle, it will iterate until Keyboard interrupt,
# adding inOctets and outOctets to the agent in the DB every 5 sec
def lifeCicle(write_api, db_bucket, addr_ip, addr_if):
    try:
        # Creating a sniffer list, used to send infoes to influx
        sniffer_list = {}

        ctr = 0
        for addrs in addr_if:
            sniff_pkt(interface=addrs, ipv4=addr_ip[ctr], sniffer_list=sniffer_list, counter=ctr)
            ctr += 1

        sleep_fun(start_time=time())

        # Infinite cicle that send info to influx about in and out packets
        while(True):
            start_time = time()
            sendValues(sniffer_list=sniffer_list, write_api=write_api, db_bucket=db_bucket)
            sleep_fun(start_time=start_time)
    except KeyboardInterrupt:
        sys.exit(0)


# Function that add values to the influx DB
def sendValues(sniffer_list, write_api, db_bucket):
    try:
        value_list = []

        #print(sniffer_list)

        for sniffer in sniffer_list.values():
            for k in sniffer.outBytesDic:
                value_list.append('outBytes,location=' + sniffer.interface + ',dst=' + k + ' bytes=' + str(sniffer.outBytesDic[k]))

            for k in sniffer.inBytesDic:
                value_list.append('inBytes,location=' + sniffer.interface + ',src=' + k + ' bytes=' + str(sniffer.inBytesDic[k]))

            for k in sniffer.outBytesDicBroad:
                value_list.append('outBytes,location=' + sniffer.interface + ',dst=255.255.255.255 bytes=' + str(sniffer.outBytesDicBroad[k]))

            for k in sniffer.inBytesDicBroad:
                value_list.append('inBytesBroad,location=' + sniffer.interface + ',src=' + k + ' bytes=' + str(sniffer.inBytesDicBroad[k]))

        #print(value_list)

        if value_list is not None:
            write_api.write(bucket=db_bucket, record=value_list)


    except KeyboardInterrupt:
        sys.exit(0)

    except:
        print('ERROR: while adding values to the database, check bucket name (-b option)')
        sys.exit(0)


# Function to let the program sleep at max for 5 sec
def sleep_fun(start_time):
    try:
        sleepTime = time() - start_time

        if sleepTime < 5:
            sleepTime = 5 - sleepTime
            sleep(sleepTime)

    except KeyboardInterrupt:
        sys.exit(0)


# Main function
def main():
    try:
        # Checking if the program is running as root
        if (os.geteuid() != 0):
            print("You need to be superuser to capture traffic")
            sys.exit(0)

        # Parsing input
        args = parsingArgs()

        # Getting info about local interfaces
        addr_if, addr_ip = getIP()

        # Connecting to DB
        db,write_api = influxDBConnection(db_url=args.db_url, db_token=args.db_token, db_org=args.db_org)

        # Starting infinite loop
        lifeCicle(write_api=write_api, db_bucket=args.db_bucket, addr_ip=addr_ip, addr_if=addr_if)
    except KeyboardInterrupt:
        sys.exit(0)


main()



