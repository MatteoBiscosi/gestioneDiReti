## SNMP System Info

### Description
The program is gonna monitor localhost interfaces and every host that is sending or receveing packets from the host and load this info on influx db.

### Requirements
For the program to run correctly, it requires:
- python3: obtainable in linux version with `sudo apt-get install python3`
- scapy: python3 library, obtainable with `pip3 install scapy`
- netifaces: python3 library, obtainable with `pip3 install netifaces`
- influxdb_client: python3 library, obtainable with `pip3 install influxdb_client`
- influx db: influx database needed, see https://www.influxdata.com/ for more info

### How to Run
Root user privilegies required to run the program. Before running check options, run `sudo ./hostMonitoring.py --help` to show run options.
It should be executable with `sudo ./hostMonitoring.py`, if it needs exec permissions (even if it should already have them) if you want to run it with ./ run the command `chmod u+x hostMonitoring.py` and after that you can run it with `sudo ./hostMonitoring.py`
Otherwise run it with `sudo python3 hostMonitoring.py`.
Run `sudo ./hostMonitoring.py --help` to show run options.
