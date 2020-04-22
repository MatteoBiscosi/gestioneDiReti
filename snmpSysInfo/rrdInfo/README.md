## SNMP System Info

### Description
The program `snmpSysInfoRRD.py` is gonna ask to the user for the various info about an snmp agent (hostname, version and community) and search for it. If the info are correct and the agent is up, the program's gonna get some general info about the agent and periodically asks for RAMs, CPUs and Disks usage (if available) and add them to an .rrd file. It's possible to see the graph of the values in the last hour with the program `snmpSysGraph.py`, that's gonna create a .png graph in graph/ directory.

### Requirements
For the program to run correctly, it requires:
- python3: obtainable in linux version with `sudo apt-get install python3`
- easysnmp: python3 library, obtainable with `pip3 install easysnmp`
- rrdtool: python3 library, obtainable with `pip3 install rrdtool`
- snmpAgent: an snmp agent reachable and configured in a way that the program che get the info about his machine

### How to Run
They should be executable with `./snmpSysInfoRRD.py` and `./snmpSysGraph.py`.
If it needs exec permissions (even if it should already have them) if you want to run it with ./ run the command `chmod +x fileName.py` and after that you can run it with `./fileName.py`
Otherwise run it with `python3 fileName.py`
