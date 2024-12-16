from scapy.layers.inet import IP, TCP, raw
from scapy.layers.l2 import srp, Ether
from scapy.all import *
import codecs
import click  # Voor een string in een editor aan te passen.
# https://click.palletsprojects.com/en/stable/api/#click.edit


class MitM:
    """
    Bij het alterneren van de load moet de user een interface met de script krijgen. Hij kan deze vervolgens aanpassen naar eigen wil.
    Het programma zal het aangepaste script terug omzetten naar de ruwe code (raw_load) en het versturen naar de ontvanger.
    """
    def __init__(self):
        self._target_ip = input('Target ip: ')
        self._gateway = input('Gateway: ')
        self._packet = None
        self._raw_load = None
        self._plain_text = None
        self._alternated_plain_text = None
        self._alternated_raw_load = None

    def get_packet(self):
        packet = sniff(count=10, filter="icmp and ip host 4.2.2.1", )

        return

    def get_raw_load(self):
        return

    def hexadec_to_plain_text(self):
        raw_load = self._raw_load

        # Convert to plain text.
        packet_data = bytes.fromhex(
            "00 1a 2b 3c 4d 5e 00 1a 2b 3c 4d 5f 08 00 45 00"
            "00 3c 1c 46 40 00 40 06 b1 e6 c0 a8 00 68 c0 a8"
            "00 01 00 50 00 50 00 00 00 00 00 00 00 00 50 02"
            "20 00 91 7c 00 00 48 65 6c 6c 6f 2c 20 57 6f 72"
            "6c 64 21"
        )

        plain_text = bytes.fromhex(packet_data).decode('utf-8')
        # Dit werkt niet, gebruik de code gemaakt door Giel!

        return

    def plain_text_to_hexdec(self):
        alternated_load = self._alternated_plain_text
        # Hier komt de code van Giel weer van pas!

        return

    def alternate_load(self):
        initial_load = self._plain_text

        def edit_sting(self, initial_load):
            """
            This function let's the user change the code decoded from the network packet.
            """
            edited_string = click.edit(text=initial_load, require_save=True)

            return edited_string

        self._alternated_plain_text = edit_sting(initial_load)
        return

    def capture(self, target_ip, gateway):
        packet = sniff(filter=f"icmp and host {target_ip}", count=2)
        print(packet.summary())

        return packet

    def send_packet(self):
        """
        For this idee, I used Copilod. See files for the composed file.
        (1) https://scapy.readthedocs.io/en/latest/usage.html
        (2) https://munich.dissec.to/kb/chapters/scapy_intro.html
        (3) https://unogeeks.com/scapy/
        (4) https://www.cs.toronto.edu/~arnold/427/18s/427_18S/indepth/scapy_wifi/scapy_tut.html
        (5) https://www.reddit.com/r/Network_Analysis/comments/77gbk2/networking_tools_101_what_is_scapy_and_how_to_use/
        (6) https://thepacketgeek.com/scapy/building-network-tools/part-06/
        """
        destination_ip = self._target_ip
        packet_load = self._alternated_raw_load

        # Contruct the network packet.
        packet = IP(dst=destination_ip)/TCP(dport=80)/packet_load

        # Sending the packet to the destination.
        send(packet)




