from scapy.all import *
from RC4_decryption_MiTM import bin_list_to_decimal_list, hex_to_8_bin_list, extend_key, generate_keystream_8_bin, decrypt


def packet_handler(pkt, bssid, WEP_key):
    if pkt.haslayer(Dot11):
        if pkt.addr2 == bssid.lower() or pkt.addr3 == bssid.lower():
            if pkt.haslayer(Dot11WEP):
                iv = pkt[Dot11WEP].iv
                print("\n=== Packet Detected ===")
                print(f"BSSID: {bssid}")
                print(f"Source: {pkt.addr2}")
                print(f"Destination: {pkt.addr1}")
                print(decrypt_packet(pkt[Dot11WEP].wepdata, iv, WEP_key))

def decrypt_packet(wepdata, iv, WEP_key):
    key_hex = iv.hex() + WEP_key.encode("utf-8").hex()
    key_ascii_list = bin_list_to_decimal_list(hex_to_8_bin_list(key_hex))
    extended_key = extend_key(key_ascii_list)
    wepdata_8_bin_list = hex_to_8_bin_list(wepdata.hex())
    keystream = generate_keystream_8_bin(extended_key, wepdata_8_bin_list)
    decrypted_packet = decrypt(keystream, wepdata_8_bin_list)
    return decrypted_packet




def start_sniffer(interface, bssid, WEP_key):
    print("Starting Sniffer")
    try:
        sniff(
            iface=interface,
            prn=lambda x: packet_handler(x, bssid, WEP_key),
            store=0
        )
    except KeyboardInterrupt:
        print("\nStopping monitor...")
    except Exception as e:
        print(f"Error: {e}")


def main():
    interface = "interface"
    bssid = "bssid"
    WEP_key = "wep key"
    start_sniffer(interface, bssid, WEP_key)
    conf.channel = 1

if __name__ == "__main__":
    main()