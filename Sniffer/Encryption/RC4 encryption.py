import pyperclip

def extend_key(key):
    key_lenght = len(key)
    extended_key = []
    for i in range(256):
        extended_key.append(key[i % key_lenght])
    return extended_key

def convert_to_ASCII(list):
    for i in range(len(list)):
        list[i] = ord(list[i])
    return list

def generate_keystream(key):
    keystream = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + keystream[j] + key[i]) % 256
        keystream[i], keystream[j] = keystream[j], keystream[i]
    return keystream

def convert_to_list(text):
    output = []
    for i in range(len(text)):
        output.append(text[i])
    return output

def convert_to_binary(list):
    for i in range(len(list)):
        list[i] = format(list[i],'08b')
    return list

def XOR(bin1, bin2):
    output_bin = ""
    for i in range(len(bin1)):
        if bin1[i] == bin2[i]:
            output_bin = output_bin + "0"
        else:
            output_bin = output_bin + "1"
    return output_bin

def adjust_keystream_length(keystream, text_list):
    while len(text_list) > len(keystream):
        keystream = keystream + keystream
    return keystream[:len(text_list)]

def crypt_bin(keystream, text):
    encrypted_bin_list = []
    for i in range(len(text)):
        encrypted_bin_list.append(XOR(keystream[i], text[i]))
    return encrypted_bin_list

def convert_to_standard(list):
    encrypted_message = ""
    for i in range(len(list)):
        char = chr(int(list[i], 2))
        encrypted_message = encrypted_message + char
    return encrypted_message

def hex_to_text(string):
    hex_string = ""

    for i in range(len(string)):
        if string[i] == "\\" or string[i] == "x":
            hex_string += ""
        else:
            hex_string += string[i]

    result_string = ''.join([chr(int(hex_string[i:i + 2], 16)) for i in range(0, len(hex_string), 2)])
    return result_string

def correct_iv(iv):
    chopped_iv = ""
    for i in range(len(iv) - 3):
        chopped_iv += iv[i + 2]
    text_iv = hex_to_text(chopped_iv)
    return chopped_iv

def encrypt():
    plain_text = input("Insert message here: ")
    text_list = convert_to_list(plain_text)
    binary_text = convert_to_binary(convert_to_ASCII(text_list))
    key = input("Insert secret key here: ")
    extended_key = extend_key(key)
    ASCII_key = convert_to_ASCII(extended_key)
    keystream = generate_keystream(ASCII_key)
    bin_keystream = convert_to_binary(keystream)
    adj_bin_ks = adjust_keystream_length(bin_keystream, binary_text)
    encrypted_bin = crypt_bin(adj_bin_ks, binary_text)
    encrypted_message = convert_to_standard(encrypted_bin)
    pyperclip.copy(encrypted_message)
    return encrypted_message, key

def decrypt(encr_message, key):
    messge_lst = convert_to_list(encr_message)
    extended_key = extend_key(key)
    ascii_key = convert_to_ASCII(extended_key)
    keystream = generate_keystream(ascii_key)
    bin_keystream = convert_to_binary(keystream)
    adj_ks = adjust_keystream_length(bin_keystream, messge_lst)
    decrypted_bin = crypt_bin(adj_ks, convert_to_binary(convert_to_ASCII(messge_lst)))
    decrypted_message = convert_to_standard(decrypted_bin)
    return decrypted_message


def main():
    encrypted_message, key = encrypt()
    print("This is the encrypted message: " + encrypted_message)
    decrypted_message = decrypt(encrypted_message, key)
    print("This is the decrypted message: " + decrypted_message)
    return

def main2():
    iv = input("dump hier de iv: ")
    hex_string = input("dump hier hexadecimal met strepen: ")
    iv = correct_iv(iv)
    key = iv + "ESAT2"
    encrypted_text = correct_iv(hex_string)
    decrypted_text = decrypt(encrypted_text, key)
    print("dit is de gedecrypteerde text " + decrypted_text)

main2()