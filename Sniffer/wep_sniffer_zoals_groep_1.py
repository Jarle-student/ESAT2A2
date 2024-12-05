from scapy.all import *
from RC4_decryption import bin_list_to_decimal_list, hex_to_8_bin_list, extend_key, generate_keystream_8_bin, decrypt


def wep_filter(packet):
    bssid = "74:DA:38:EB:6F:DC"
    if packet.haslayer(Dot11):
        return (packet.addr1 == bssid or packet.addr2 == bssid or packet.addr3 == bssid)
    return False

def decrypt_packet(wepdata, iv, WEP_key):
    key_hex = iv.hex() + WEP_key.encode("utf-8").hex()
    key_ascii_list = bin_list_to_decimal_list(hex_to_8_bin_list(key_hex))
    extended_key = extend_key(key_ascii_list)
    wepdata_8_bin_list = hex_to_8_bin_list(wepdata.hex())
    keystream = generate_keystream_8_bin(extended_key, wepdata_8_bin_list)
    decrypted_packet = decrypt(keystream, wepdata_8_bin_list)
    return decrypted_packet

def packet_handler(packet, wep_key):
    if packet.haslayer(Dot11):
        print("WEP", packet.FCfield & 0b01000000 != 0)
    
    if packet.haslayer(Dot11WEP):
        iv = packet[Dot11WEP].iv
        enc_data = packet[Dot11WEP].wepdata
        decr_data = decrypt_packet(enc_data, iv, wep_key)
        print(f"Decrypted data: {decr_data}")

    else:
        print("No WEP-encryption")


    pass

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
    interface = "wlan0"
    start_sniffer(interface, wep_key)

if __name__ == "__main__":
    main()
