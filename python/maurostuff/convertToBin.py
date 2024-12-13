import numpy as np

def convert_cu8_to_bin(cu8_file, bin_file):
    """
    Converteer een CU8 bestand naar een binair bestand.
    
    :param cu8_file: Het pad naar het CU8 bestand.
    :param bin_file: Het pad waar het gegenereerde bin bestand opgeslagen moet worden.
    """
    # Lees CU8-bestand als een array van unsigned 8-bit integers (0-255)
    cu8_data = np.fromfile(cu8_file, dtype=np.uint8)

    # Sla de data op in binair formaat
    cu8_data.tofile(bin_file)

    print(f"CU8 data is omgezet naar {bin_file}")

# Voorbeeld van gebruik
cu8_file = 'input_file.cu8'  # Pad naar je CU8-bestand
bin_file = 'output_file.bin'  # Pad waar je het bin-bestand wilt opslaan

convert_cu8_to_bin(cu8_file, bin_file)
