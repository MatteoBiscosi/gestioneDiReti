#!/usr/bin/python3

# Import
import rrdtool
import os.path
from os import mkdir
from time import time
from time import sleep
from easysnmp import Session
from easysnmp import EasySNMPConnectionError


# This function print all the system's info, if it isn't reachable, will terminate the program
# if system info aren't available but the system is reachable then it will print the right message
# but won't stop the program
def printSysInfo(hostname, version, community):
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


# Function that controls the flow of the various functions that prints CPU, Ram and Disk info
def printStats(hostname, version, community, session):

    # Checking if the directory and files exist otherwise it's gonna create them
    dir, cpu, ram, disk = checkRrd(session = session)

    # Problems while creating the file, program shutting down
    if not dir:
        print("ERROR: Problem while creating the necessary files, the program will now terminate.")
        exit(1)

    else:
        if not cpu and not disk and not ram:
            print("ERROR: Problem while creating the necessary files, the program will now terminate.")
            exit(1)

    # Files created, starting the update cicle
    currentTime = time()

    cpuAvailable = False
    ramAvailable = False
    diskAvailable = False

    if cpu:
        cpuAvailable = printCpu(hostname=hostname, version=version, community=community, session=session)

    if ram:
        ramAvailable = printRam(hostname=hostname, version=version, community=community, session=session)

    if disk:
        diskAvailable = printDisk(hostname=hostname, version=version, community=community, session=session)

    # Checking that at last an info is available
    if cpuAvailable is False and ramAvailable is False and diskAvailable is False:
        print("ERROR: None of the system info is accessible, the program will now terminate.")
        exit(1)

    #print("\t", cpuAvailable, "\n\t", ramAvailable, "\n\t", diskAvailable, "\n")

    iterations = 719
    seconds = 5

    while(iterations > 1):
        sleepTime = time() - currentTime

        if sleepTime < seconds:
            sleepTime = seconds - sleepTime

            try:
                sleep(sleepTime)
            except KeyboardInterrupt:
                print("ERROR: Program interrupted from the user.")
                exit(1)

        currentTime = time()

        if cpuAvailable is True:
            cpuAvailable = printCpu(hostname=hostname, version=version, community=community, session=session)

        if ramAvailable is True:
            ramAvailable = printRam(hostname=hostname, version=version, community=community, session=session)

        if diskAvailable is True:
            diskAvailable = printDisk(hostname=hostname, version=version, community=community, session=session)

        iterations -= 1
        #print("\t", cpuAvailable, "\n\t", ramAvailable, "\n\t", diskAvailable, "\n")


# Function used to print CPU info
def printCpu(hostname, version, community, session):
    try:
        rsp = session.get('.1.3.6.1.4.1.2021.11.9.0')
        rrdtool.update(
            "./rrdLogs/cpu.rrd",
            "N:" + rsp.value)
    except:
        return False

    return True


# Function used to print Ram info
def printRam(hostname, version, community, session):
    try:
        rsp = session.get('.1.3.6.1.4.1.2021.4.6.0')
        rrdtool.update(
            "./rrdLogs/ram.rrd",
            "N:" + rsp.value)
    except:
        return False

    return True


# Function used to print Disk info
def printDisk(hostname, version, community, session):
    try:
        rsp = session.get('.1.3.6.1.4.1.2021.9.1.10.1')
        rrdtool.update(
            "./rrdLogs/disk.rrd",
            "N:" + rsp.value)
    except:
        return False

    return True


# Function used to check if the log's directory and the various .rrd files exists
# if not it's gonna create them
def checkRrd(session):

    dir, cpu, ram, disk = True, True, True, True

    if os.path.isdir("./rrdLogs"):
        if not os.path.exists("./rrdLogs/cpu.rrd"):
            cpu = createCpu()

        if not os.path.exists("./rrdLogs/ram.rrd"):
            ram = createRam(session)

        if not os.path.exists("./rrdLogs/disk.rrd"):
            disk = createDisk()
    else :
        dir = createDir()
        cpu = createCpu()
        ram = createRam(session)
        disk = createDisk()

    if dir:
        return dir, cpu, ram, disk

    return False, False, False, False


# Function that creates the directory for .rrd files
def createDir():
    try:
        os.mkdir("./rrdLogs")
    except:
        return False

    return True


# Function that create cpu .rrd file
def createCpu():
    try:
        rrdtool.create(
            "./rrdLogs/cpu.rrd",
            "--start", "now",
            "--step", "5",
            "DS:cpu:GAUGE:10:0:100",
            "RRA:AVERAGE:0.5:1:17280",
            "RRA:HWPREDICT:360:0.1:0.0035:288"
        )
    except:
        return False

    return True


# Function that create cpu .rrd file
def createRam(session):
    try:
        rsp = session.get(".1.3.6.1.4.1.2021.4.5.0")
        rrdtool.create(
            "./rrdLogs/ram.rrd",
            "--start", "now",
            "--step", "5",
            "DS:ram:GAUGE:10:0:" + rsp.value,
            "RRA:AVERAGE:0.5:1:17280",
            "RRA:HWPREDICT:360:0.1:0.0035:288"
        )
    except:
        return False

    return True


# Function that create cpu .rrd file
def createDisk():
    try:
        rrdtool.create(
            "./rrdLogs/disk.rrd",
            "--start", "now",
            "--step", "5",
            "DS:disk:GAUGE:10:0:100",
            "RRA:AVERAGE:0.5:1:17280",
            "RRA:HWPREDICT:360:0.1:0.0035:288"
        )
    except:
        return False

    return True


# Main function, here the program requests all the necessary input and starts the
# necessary functions
def main():
    hostname = "localhost"
    community = "public"
    version = 1

    # Here, gonna check if the user wants the standard variables or not
    print("Standard values set as:\nhostname = localhost\ncommunity = public\nversion = 1")
    print("Do you want to change them?y/n")

    rsp = input()

    while rsp != 'y' and rsp != 'n':
        print("Please insert y or n...")
        rsp = input()

    # if he wants to change them, i'm gonna let him insert the hostname, version and community
    if rsp == 'y':
        hostname = input("Enter the hostname: ")
        version = input("Enter the snmp version: ")
        community = input("Enter the community: ")

        # version check, if he inserted a valid number (greater then 0 and 1,2 or 3)
        try:
            version = int(version)
        except ValueError:
            print("Invalid number; please insert a valid number...")
        while version != 1 and version != 2 and version != 3:
            print("Invalid version; please choose between version 1 and 2...")
            version = input("Enter the snmp version: ")
            try:
                version = int(version)
            except ValueError:
                print("Invalid number; please insert a valid number...")

    # Checking agent info and taking the session
    session = printSysInfo(hostname=hostname, version=version, community=community)

    printStats(hostname=hostname, version=version, community=community, session=session)


main()
