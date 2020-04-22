#!/usr/bin/python3

# Import
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
        print("Invalid hostname or community.")
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
def printStats(hostname, version, community, iterations, session, seconds):

    currentTime = time()

    print("\n### Measurement n.: 1/", iterations, " ###")

    cpuAvailable = printCpu(hostname=hostname, version=version, community=community, session=session)
    ramAvailable = printRam(hostname=hostname, version=version, community=community, session=session)
    diskAvailable = printDisk(hostname=hostname, version=version, community=community, session=session)

    # Checking that at last an info is available
    if cpuAvailable is False and ramAvailable is False and diskAvailable is False:
        print("None of the system info is accessible, the program will now terminate.")
        exit(1)

    tmp = iterations

    while(tmp > 1):
        sleepTime = time() - currentTime

        if sleepTime < seconds:
            sleepTime = seconds - sleepTime

            try:
                sleep(sleepTime)
            except KeyboardInterrupt:
                print("Program interrupted from the user.")
                exit(1)

        currentTime = time()

        print("\n### Measurement n.: ", tmp, "/", iterations, " ###")

        if cpuAvailable is True:
            printCpu(hostname=hostname, version=version, community=community, session=session)

        if ramAvailable is True:
            printRam(hostname=hostname, version=version, community=community, session=session)

        if diskAvailable is True:
            printDisk(hostname=hostname, version=version, community=community, session=session)

        tmp -= 1


# Function used to print CPU info
def printCpu(hostname, version, community, session):
    try:
        print("\nCPU\n")
        rsp = session.get('.1.3.6.1.4.1.2021.10.1.3.1')
        print("CPU 1 min load: ", rsp.value)
        rsp = session.get('.1.3.6.1.4.1.2021.11.9.0')
        print("percentage of user CPU time: ", rsp.value)
        rsp = session.get('.1.3.6.1.4.1.2021.11.11.0')
        print("percentages of idle CPU time: ", rsp.value)
    except:
        return False

    return True


# Function used to print Ram info
def printRam(hostname, version, community, session):
    try:
        print("\nRAM\n")
        rsp = session.get('.1.3.6.1.4.1.2021.4.6.0')
        print("Total RAM used: ", rsp.value)
        rsp = session.get('.1.3.6.1.4.1.2021.4.11.0')
        print("Total RAM Free: ", rsp.value)
        rsp = session.get('.1.3.6.1.4.1.2021.4.15.0')
        print("Total Cached Memory: ", rsp.value)
    except:
        return False

    return True


# Function used to print Disk info
def printDisk(hostname, version, community, session):
    try:
        print("\nDISK\n")
        rsp = session.get('.1.3.6.1.4.1.2021.9.1.9.1')
        print("DISK percentage of space used: ", rsp.value)
        rsp = session.get('.1.3.6.1.4.1.2021.9.1.10.1')
        print("Percentage of inodes used on DISK: ", rsp.value)
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

    # Asking how many iterations he wants
    print("\nHow many iterations do you want to do?")
    while True:
        iterations = input()
        try:
            iterations = int(iterations)

            if iterations < 0:
                print("Please insert a number of iterations greater then 0...")
            break
        except ValueError:
            print("Invalid number; please insert a valid number...")

    # Asking how much seconds should pass between two measurements
    print("\nHow much seconds should be the interval between measurements?")
    while True:
        seconds = input()
        try:
            seconds = int(seconds)
            if seconds < 0:
                print("Please insert a number greater then 0...")
                continue
            break
        except ValueError:
            print("Invalid number; please insert a valid number...")

    if seconds > 0 and iterations > 0:
        printStats(hostname=hostname, version=version, community=community,
                   iterations=iterations, session=session, seconds=seconds)


main()
