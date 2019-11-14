#!usr/bin/python3
#hooray github repository is now working!!!

import subprocess
import optparse


def change_mac(interface, new_mac):
    print('[+] Changing MAC address for ' + interface + ' to ' + new_mac)

    subprocess.call(['ifconfig', interface, 'down'])
    subprocess.call(['ifconfig', interface, 'hw', 'ether', new_mac])
    subprocess.call(['ifconfig', interface, 'up'])


parser = optparse.OptionParser()
parser.add_option('-i', '--interface', dest='interface',
                  help='Interface to change the MAC address')
parser.add_option('-m', '--mac', dest='new_mac', help='The New MAC address')

(options, arguments) = parser.parse_args()

change_mac(options.interface, options.new_mac)

