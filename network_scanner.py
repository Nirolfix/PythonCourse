#!usr/bin/python3
import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target',
                      help='Target IP or IP range.')
    options = parser.parse_args()
    if not options.target:
        parser.error(
            '[-] Please specify a target IP or IP range, use --help for more info.')
    return options

def scan(ip):
    # scapy.arping(ip)
    # prepare the packet to send all over the network
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst='ff:ff:ff:ff:ff:ff')

    # send the packet to the network and receive the answer
    arp_request_broadcast = broadcast/arp_request
    ansewered_list = scapy.srp(
        arp_request_broadcast, timeout=1, verbose=False)[0]


    # parse the answer into list of dictionaries
    clients_list=[]
    for element in ansewered_list:
        client_dict =  {'ip': element[1].psrc, 'mac': element[1].hwsrc}
        clients_list.append(client_dict)
        # print(element[1].psrc + '\t\t' + element[1].hwsrc)
    return(clients_list)

def print_result(results_list):
    # print the header
    print('IP\t\t\tMAC Address\n______________________________________________')
    for client in results_list:
        print(client['ip'] + '\t\t' + client['mac'])

options = get_arguments()
scan_result = scan(options.target)
print_result(scan_result)