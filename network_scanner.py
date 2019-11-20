#!usr/bin/python
import scapy.all as scapy


def scan(ip):
    scapy.arping(ip)
    # arp_request = scapy.ARP(pdst=ip)
    # arp_request.show()
    # broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')
    # broadcast.show()
    # arp_request_broadcast = broadcast/arp_request
    # arp_request_broadcast.show()
    # # scapy.ls(scapy.Ether())


scan('192.168.9.161/24')
