import subprocess

def manchester_encode(data):
    encoded = ''
    for bit in data:
        if bit == '0':
            encoded += '01'
        else:
            encoded += '10'
    return encoded

# TPMS packet in hex (Preamble + Sensor ID + Pressure + Temp + Status + CRC)
tpms_packet_hex = "AA AA AA 82 D1 41 98 EC 08 01 4F"

# Omzetten naar binaire data
binary_data = bin(int(tpms_packet_hex.replace(" ", ""), 16))[2:].zfill(len(tpms_packet_hex.replace(" ", "")) * 4)

# Manchester encoderen
encoded_data = manchester_encode(binary_data)

# Omzetten naar bytes
encoded_bytes = int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, byteorder='big')

# Opslaan als binair bestand
with open("tpms_signal.bin", "wb") as f:
    f.write(encoded_bytes)

# HackRF configuratie: 433.92 MHz, 250 kHz bandwidth
subprocess.run([
    "hackrf_transfer",
    "-t", "tpms_signal.bin",  # bestand met signaal
    "-f", "433920000",        # frequentie in Hz (433.92 MHz)
    "-s", "2000000",          # sample rate (2 MS/s)
    "-a", "1",                # antenne aanzetten
    "-x", "0"                 # zendvermogen (0-47 dB)
])
