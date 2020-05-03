from scapy.all import *
from scapy import route
from scapy.layers.inet import Ether,IP,UDP
from threading import Thread
from time import sleep


class Sniffer(Thread):
    def __init__(self, interface="eth0", ipv4='127.0.0.1'):
        super().__init__()
        self.interface = interface
        self.ipv4 = ipv4
        self.pktLosses = 0
        self.outBytesDic = {}
        self.inBytesDic = {}
        self.outBytesDicBroad = {}
        self.inBytesDicBroad = {}
        self.lo = 0

    def run(self):
        sniff(iface=self.interface, prn=self.add_packet)

    def add_packet(self, packet):
        try:
            ip_layer = packet.getlayer(IP)
            if ip_layer is not None:
                src_ip = ip_layer.src
                dst_ip = ip_layer.dst
                #print("[!] New Packet: {src} -> {dst}".format(src=ip_layer.src, dst=ip_layer.dst))

                if src_ip == self.ipv4:
                    self.outBytesDic[dst_ip] = self.outBytesDic.get(dst_ip, 0) + packet.len

                elif dst_ip == self.ipv4:
                    self.inBytesDic[src_ip] = self.inBytesDic.get(src_ip, 0) + packet.len

                elif dst_ip == '255.255.255.255' and src_ip is not self.ipv4:
                    self.inBytesDicBroad[src_ip] = self.inBytesDicBroad.get(src_ip, 0) + packet.len

                elif dst_ip == '255.255.255.255' and src_ip == self.ipv4:
                    self.outBytesDicBroad[self.ipv4] = self.outBytesDicBroad.get(self.ipv4, 0) + packet.len

        except AttributeError:
            self.pktLosses += 1


#sniffer = {}
#sniffer[0] = Sniffer(interface='eth0', ipv4='192.168.1.11')

#sniffer[0].start()
#while True:
 #   sleep(5)
  #  print(sniffer[0].outBytesDic)
   # print(sniffer[0].inBytesDic)
    #print(sniffer[0].inBytesDicBroad)
    #print(sniffer[0].outBytesDicBroad)
    #print(sniffer[0].pktLosses)
    #print(sniffer[0].lo)
