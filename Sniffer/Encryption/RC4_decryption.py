### CODE FOR RC4 DECRYPTION ###

### makes the hexadecimal go into a list with in each entry one byte
def hex_get_listed(hex):
    list = []
    for i in range(0, len(hex), 2):
        list.append(hex[i:i+2])
    return list

### the logical XOR operator
def XOR(bin1, bin2):
    output_bin = ""
    for i in range(len(bin1)):
        if bin1[i] == bin2[i]:
            output_bin = output_bin + "0"
        else:
            output_bin = output_bin + "1"
    return output_bin

### converts a hexidecimal into an 8-digit-binary list
def hex_to_8_bin_list(hex):
    hex_list = hex_get_listed(hex)
    bin_list = []
    for hexi in hex_list:
        bin_list.append("{0:08b}".format(int(hexi, 16)))
    return bin_list

### converts a binary list to a text list
def bin_to_text_string(bin_list):
    text = ""
    for i in range(len(bin_list)):
        char = chr(int(bin_list[i], 2))
        text += char
    return text

### converts a binary list to decimal list
def bin_list_to_decimal_list(bin_list):
    ascii_list = []
    for bin in bin_list:
        ascii_list.append(int(bin, 2))
    return ascii_list

### converts a decimal list to binary list
def decimal_list_to_bin_list(decimal_list):
    bin_list = []
    for deci in decimal_list:
        bin_list.append(format(deci, '08b'))
    return bin_list

### extends the key to 256 bytes
def extend_key(key):
    key_lenght = len(key)
    extended_key = []
    for i in range(256):
        extended_key.append(key[i % key_lenght])
    return extended_key

### generates a keystream using the extended key and turns it into 8-digit-binary.
### it also gives the keystream the desired length to decrypt the packet.
def generate_keystream_8_bin(extended_key, encrypted_packet_list):
    keystream = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + keystream[j] + extended_key[i]) % 256
        keystream[i], keystream[j] = keystream[j], keystream[i]

    while len(encrypted_packet_list) > len(keystream):
        keystream = keystream + keystream
    return decimal_list_to_bin_list(keystream[:len(encrypted_packet_list)])

### decrypts the encrypted packet using the keystream and the XOR operator
def decrypt(keystream, encrypted_packet):
    decrypted_bin_list = []
    for i in range(len(encrypted_packet)):
        decrypted_bin_list.append(XOR(keystream[i], encrypted_packet[i]))
    decrypted_packet = bin_to_text_string(decrypted_bin_list)
    return decrypted_packet

def main():
    ### INITIALIZING THE KEY ###
    iv_b = b'\x9a\x02\x00'
    key_hex = iv_b.hex() + "4553415432"
    key_ascii_list = bin_list_to_decimal_list(hex_to_8_bin_list(key_hex))
    extended_key = extend_key(key_ascii_list)


    ### INITIALIZING THE PACKET ###
    encrypted_packet_b = b',\xa1YoJ\x87\x80\xf2q\x85A\x10;\xaa/}'
    encrypted_packet_8_bin_list = hex_to_8_bin_list(encrypted_packet_b.hex())


    ### DECRYPTING THE PACKET ###
    keystream = generate_keystream_8_bin(extended_key, encrypted_packet_8_bin_list)
    decrypted_packet = decrypt(keystream, encrypted_packet_8_bin_list)
    print(decrypted_packet)

    return

main()