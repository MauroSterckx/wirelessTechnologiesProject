import numpy as np

# Data in bytes (omgezet van de tekst)
data = b"Abarth-124Spider TPMS id c15a6b6f flags 00 Pressure 273 kPa Temperature 16 C status 72 Integrity CHECKSUM"

# Converteer de byte-data naar een gestructureerde IQ-voorstelling (bijv. FSK-modulatie)
# Dit is een simpele simulatie van het proces, het moet aangepast worden voor daadwerkelijke modulatie
iq_data = np.zeros(len(data) * 2)  # I en Q componenten, 2 voor elk byte

# Vul IQ data (voor de eenvoud vullen we met gesimuleerde data)
for i in range(len(data)):
    iq_data[2*i] = (data[i] & 0xF0) / 255.0  # I component
    iq_data[2*i+1] = (data[i] & 0x0F) / 255.0  # Q component

# Converteer naar complex getal en sla op
iq_data = iq_data.astype(np.float32)
iq_data_complex = iq_data[::2] + 1j * iq_data[1::2]

# Sla op als IQ-bestand
iq_data_complex.tofile("tpms_iq_data.bin")
