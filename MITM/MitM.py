from scapy.layers.l2 import srp, Ether
from scapy.all import sniff
import codecs

class MitM:
    """
    Bij het alterneren van de load moet de user een interface met de script krijgen. Hij kan deze vervolgens aanpassen naar eigen wil.
    Het programma zal het aangepaste script terug omzetten naar de ruwe code (raw_load) en het versturen naar de ontvanger.
    """
    def __init__(self):
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
        return

    def alternate_load(self):
        return

    def send(self):
        return



