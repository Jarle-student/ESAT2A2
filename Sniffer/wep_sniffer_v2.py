from scapy.all import *
from RC4_decryption import bin_list_to_decimal_list, hex_to_8_bin_list, extend_key, generate_keystream_8_bin, decrypt
"""
Don't forget
sudo iwconfig wlan0mon channel 1
"""

### Filter for Dot11 and MAC address
def wep_filter(packet):
    bssid = "B8:27:EB:A7:6C:47"
    if packet.haslayer(Dot11):
        return (packet.addr1 == bssid.lower() or packet.addr2 == bssid.lower() or packet.addr3 == bssid.lower())
    return False

### Decrypt the wepdata
def decrypt_packet(wepdata, iv, WEP_key):
    key_hex = iv.hex() + WEP_key.encode("utf-8").hex()
    key_ascii_list = bin_list_to_decimal_list(hex_to_8_bin_list(key_hex))
    extended_key = extend_key(key_ascii_list)
    wepdata_8_bin_list = hex_to_8_bin_list(wepdata.hex())
    keystream = generate_keystream_8_bin(extended_key, wepdata_8_bin_list)
    decrypted_packet = decrypt(keystream, wepdata_8_bin_list)
    return decrypted_packet

### Process the packet
def packet_handler(packet, wep_key):
    ### WEP encryption
    if packet.haslayer(Dot11WEP):
        iv = packet[Dot11WEP].iv
        enc_data = packet[Dot11WEP].wepdata
        decr_data = decrypt_packet(enc_data, iv, wep_key)
        print(f"Decrypted data: {decr_data}")

    ### No WEP encryption, only Dot11
    else:
        print("No WEP-encryption")

### Start the sniffer
def start_sniffer(interface, wep_key):
    print(f"Sniffing on interface: {interface}")
    try:
        sniff(iface = interface, 
              prn = lambda x: packet_handler(x, wep_key), 
              lfilter = wep_filter
              )
        
    except Exception as e:
        print(f"Error: {e}")

def main():
    wep_key = "ESAT2"
    interface = "wlan0mon"
    start_sniffer(interface, wep_key)

if __name__ == "__main__":
    main()
