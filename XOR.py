# Hex string variable
hex_s = '653cae8da8edb426052'

# Plain text variable
plain = ''

# variable to store the XOR of previous digits
xor = 0

l = len(hex_s)

# Loop for loop from the end to the mid section of the string
for i in range(l - 1, int(l / 2) - 1, -1):

    # Calculation of the plaintext digit
    y = xor^int(hex_s[i], 16)  # base = 16

    # Calculation of XOR chain
    xor = xor^y
    plain = hex(y)[-1] + plain

print(plain)
