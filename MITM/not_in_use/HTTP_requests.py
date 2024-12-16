"""from scapy.all import *
from scapy.layers.http import HTTPRequest, HTTPResponse

def packet_callback(packet):
    if packet.haslayer(HTTPRequest):
        http_request = packet[HTTPRequest]
        print(f"HTTP Request: {http_request.Method} {http_request.Path}")
    elif packet.haslayer(HTTPResponse):
        http_response = packet[HTTPResponse]
        print(f"HTTP Response: {http_response.Status_Code} {http_response.Reason_Phrase}")
        print(packet[Raw].load)
    elif packet.haslayer(Raw):
        payload = packet[Raw].load
        try:
            payload_decoded = payload.decode(errors='ignore')
            if "HTTP/1.1 200 OK" in payload_decoded:
                print(f"HTTP Response Load: \n{payload_decoded}")
        except UnicodeDecodeError as e:
            print(f"Decoding error: {e}")

# Capture packets and reassemble TCP streams
sniff(prn=packet_callback, filter="tcp port 80", store=0, session=TCPSession)"""


from scapy.all import *
from scapy.layers.inet import TCP
from scapy.layers.http import HTTPRequest
import html
import click

# Dictionary to store TCP streams
http_responses = {}


def format_html(html_content):
    # Use html.unescape to handle HTML entities for better readability
    #print(html.escape(html_content))
    return html.unescape(html_content)


def packet_callback(packet):

    if packet.haslayer(HTTPRequest):
        http_request = packet[HTTPRequest]
        print(http_request.Method)
        print(f"HTTP Request: {http_request.Method.decode()} {http_request.Path.decode()}")
    elif packet.haslayer(TCP):
        tcp = packet[TCP]
        stream_index = (tcp.sport, tcp.dport, tcp.seq, tcp.ack)

        # Reassemble TCP stream
        if stream_index not in http_responses:
            http_responses[stream_index] = b""
        if packet.haslayer(Raw):
            payload = packet[Raw].load
            http_responses[stream_index] += payload

            try:
                # Attempt to decode and find the HTTP response in the reassembled stream
                payload_decoded = http_responses[stream_index].decode(errors='ignore')
                headers_end_idx = payload_decoded.find('\r\n\r\n')
                if headers_end_idx != -1:
                    entity_body = payload_decoded[headers_end_idx + 4:]
                    # Format and print HTML content
                    print("HTTP Response Entity Body (Formatted HTML):")
                    formatted_body = format_html(entity_body)
                    print(formatted_body)
                    new_formatted_body = click.edit(formatted_body, editor='notepad')
                    #send(new_formatted_body)

                    # Clear the stored response after printing
                    del http_responses[stream_index]
                else:
                    print("Headers end not found in payload.")
                    print(payload_decoded)
            except UnicodeDecodeError as e:
                print(f"Decoding error: {e}")


# Capture packets and reassemble TCP streams
sniff(prn=packet_callback, filter="tcp port 3000", store=0, session=TCPSession)

