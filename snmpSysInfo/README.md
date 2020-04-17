## SNMP System Info

### Description
The program is gonna ask to the user for the various info about an snmp agent (hostname, version and community) and search for it. If the info are correct and the agent is up, the program's gonna get some general info about the agent and periodically asks for various RAMs, CPUs, Disks info (if available)

### Requirements
For the program to run correctly, it requires:
- python3: obtainable in linux version with sudo apt-get install python3
- easysnmp: python3 library, obtainable with pip3 install easysnmp
- snmpAgent: an snmp agent reachable and configured in a way that the program che get the info about his machine

### How to Run
It needs exec permissions if you want to run it with ./ so run the command chmod +x snmpSysInfo.py and after that you can run it with <./snmpSysInfo.py>
Otherwise run it with python3 snmpSysInfo.py
