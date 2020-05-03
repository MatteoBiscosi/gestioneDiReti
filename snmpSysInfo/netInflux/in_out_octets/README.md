## SNMP System Info

### Description
The program is gonna ask to the user for the various info about an snmp agent (hostname, version and community) and search for it. If the info are correct and the agent is up, the program's gonna get some general info about the agent and periodically asks for InOctets and OutOctets info (if available) and load them on the influx db.

### Requirements
For the program to run correctly, it requires:
- python3: obtainable in linux version with `sudo apt-get install python3`
- easysnmp: python3 library, obtainable with `pip3 install easysnmp`
- snmpAgent: an snmp agent reachable and configured in a way that the program che get the info about his machine
- influxdb_client: python3 library, obtainable with `pip3 install influxdb_client`
- influx db: influx database needed, see [influxdb](https://www.influxdata.com/) for more info

### How to Run
It should be executable with `./snmpNetInfoInflux.py`.
If it needs exec permissions (even if it should already have them) if you want to run it with ./ run the command `chmod +x snmpNetInfoInflux.py` and after that you can run it with `./snmpNetInfoInflux.py`
Otherwise run it with `python3 snmpNetInfoInflux.py`.
Run `./snmpNetInfoInflux.py --help` to show run options.
