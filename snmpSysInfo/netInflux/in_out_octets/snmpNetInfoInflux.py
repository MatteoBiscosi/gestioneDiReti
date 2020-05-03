#!/usr/bin/python3

# Import
import argparse
from time import time
from time import sleep
from easysnmp import Session
from easysnmp import EasySNMPConnectionError
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS


# Function used to parse input arguments; arguments options:
#   - v : version, default value: '1'
#   - c : community, default value: 'community'
#   - i : ip, default value 'localhost'
def parsingArgs():
    parser = argparse.ArgumentParser(description='Tool used to analize an snmp agent netstat')

    parser.add_argument('-v', choices=[1, 2, 3], metavar=1, type=int, nargs='?', default=1, dest='version',
                        help='snmp version: 1, 2, 3')

    parser.add_argument('-c', metavar='systemonly', type=str, nargs='?', default='public', dest='community',
                        help='snmp community')

    parser.add_argument('-i', metavar='localhost', type=str, nargs='?', default='localhost', dest='hostname',
                        help='snmp hostname')

    parser.add_argument('-u', metavar='url', type=str, nargs='?', default='https://us-central1-1.gcp.cloud2.influxdata.com', dest='db_url',
                        help='influxDB url')

    parser.add_argument('-t', metavar='token', type=str, nargs='?', default='yHmDok5I-FnSlPkxous9ecUktp6rh3Jy8g0k48wQnhACLUOnsmPKZV5EED1wqzYmoOo32iaLoyzKM4tV77VkqA==', dest='db_token',
                        help='influxDB token')

    parser.add_argument('-o', metavar='organization', type=str, nargs='?', default='m.biscosi', dest='db_org',
                        help='influxDB organization')

    parser.add_argument('-b', metavar='bucket', type=str, nargs='?', default='localhost', dest='db_bucket',
                        help='influxDB bucket')

    args = parser.parse_args()

    return args


# Function used to connect to the snmp agent
def snmpConnection(version, community, hostname):
    try:
        session = Session(hostname=hostname, community=community, version=version)
    except EasySNMPConnectionError:
        print("ERROR: Invalid hostname or community.")
        exit(1)

    try:
        info = session.get('sysName.0')
        print("\nName: ", info.value)
        info = session.get('sysLocation.0')
        print("Location: ", info.value)
        info = session.get('sysDescr.0')
        print("Description: ", info.value)
        info = session.get('sysObjectID.0')
        print("ID: ", info.value)
        info = session.get('sysContact.0')
        print("Contact: ", info.value)
    except:
        print("\nSystem info aren't available")

    return session


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


# Application cicle, it will iterate until Keyboard interrupt,
# adding inOctets and outOctets to the agent in the DB every 5 sec
def lifeCicle(agent, db, write_api, db_bucket, agent_loc):
    try:
        while(True):
            start_time = time()
            inOctets, outOctets = getOctets(agent=agent)
            addValue(inOctets=inOctets, outOctets=outOctets, db=db, write_api=write_api, db_bucket=db_bucket, agent_loc=agent_loc)
            sleep_fun(start_time=start_time)
    except KeyboardInterrupt:
        exit(1)


# Function that get in and out Octets from the snmp Agent
def getOctets(agent):
    try:
        rspIn = agent.get('.1.3.6.1.2.1.2.2.1.16.1')
        rspOut = agent.get('.1.3.6.1.2.1.2.2.1.16.2')
    except:
        print("ERROR: inOctets and outOctets aren't available. Shutting down...")
        exit(1)

    return rspIn.value, rspOut.value


# Function that add values to the influx DB
def addValue(inOctets, outOctets, db, write_api, db_bucket, agent_loc):
    try:
        # InOctets values
        value = Point("inOctets").tag("location", agent_loc).field("bytes", int(inOctets))
        write_api.write(bucket=db_bucket, record=value)

        # OutOctets values
        value = Point("outOctets").tag("location", agent_loc).field("bytes", int(outOctets))
        write_api.write(bucket=db_bucket, record=value)
    except KeyboardInterrupt:
        exit(1)

    except:
        print('ERROR: while adding values to the database, check bucket name (-b option)')
        exit(1)


# Function to let the program sleep at max for 5 sec
def sleep_fun(start_time):
    sleepTime = time() - start_time

    if sleepTime < 5:
        sleepTime = 5 - sleepTime

        try:
            sleep(sleepTime)
        except KeyboardInterrupt:
            exit(1)


# Main function
def main():
    try:
        args = parsingArgs()
        snmpAgent = snmpConnection(version=args.version, community=args.community, hostname=args.hostname)
        db,write_api = influxDBConnection(db_url=args.db_url, db_token=args.db_token, db_org=args.db_org)
        lifeCicle(agent=snmpAgent, db=db, write_api=write_api, db_bucket=args.db_bucket, agent_loc=args.hostname)
    except KeyboardInterrupt:
        exit(1)


main()