import subprocess

# TPMS packet in hex (Preamble + Sensor ID + Pressure + Temp + Status + CRC)
tpms_packet_hex = "AA AA AA 82 D1 41 98 EC 08 01 4F"

# Omzetten naar binaire data
tpms_packet_bytes = bytes.fromhex(tpms_packet_hex.replace(" ", ""))

# Opslaan als binair bestand
with open("tpms_signal.bin", "wb") as f:
    f.write(tpms_packet_bytes)

# HackRF configuratie: 433.92 MHz, 250 kHz bandwidth
subprocess.run([
    "hackrf_transfer",
    "-t", "tpms_signal.bin",  # bestand met signaal
    "-f", "433920000",        # frequentie in Hz (433.92 MHz)
    "-s", "2000000",          # sample rate (2 MS/s)
    "-a", "1",                # antenne aanzetten
    "-x", "0"                 # zendvermogen (0-47 dB)
])
