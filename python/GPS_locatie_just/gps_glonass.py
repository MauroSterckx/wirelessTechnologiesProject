import serial
import pynmea2

# Functie om NMEA latitude/longitude om te zetten naar decimale graden
def convert_to_decimal(degrees_minutes, direction):
    if not degrees_minutes or not direction:
        # Controleer of de input geldig is
        raise ValueError("Invalid NMEA data: degrees_minutes or direction is empty.")

    # Splits graden en minuten
    degrees = int(float(degrees_minutes) // 100)
    minutes = float(degrees_minutes) % 100
    decimal = degrees + (minutes / 60)
    
    # Pas de richting toe (S of W is negatief)
    if direction in ['S', 'W']:
        decimal = -decimal
    return round(decimal, 6)

# Functie om de eerste NMEA-zin met locatiegegevens te lezen
def get_gps_coordinates(port, baudrate=9600, timeout=1):
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as stream:
            print(f"Listening for NMEA data on {port} at {baudrate} baud...")
            # Lees één regel van de seriële poort
            while True:  # Blijf proberen totdat een geldige NMEA-zin wordt gevonden
                line = stream.readline().decode('ascii', errors='ignore').strip()
                if line.startswith('$'):  # Controleer of het een NMEA-zin is
                    try:
                        msg = pynmea2.parse(line)  # Parse de NMEA-zin
                        if hasattr(msg, 'lat') and hasattr(msg, 'lon'):
                            # Controleer of latitude en longitude niet leeg zijn
                            if msg.lat and msg.lon:
                                # Converteer latitude en longitude naar decimale graden
                                lat = convert_to_decimal(msg.lat, msg.lat_dir)
                                lng = convert_to_decimal(msg.lon, msg.lon_dir)
                                return {"lat": lat, "lng": lng}
                            else:
                                print("Incomplete latitude/longitude data. Waiting for valid signal...")
                        else:
                            print("No latitude/longitude data in the received NMEA sentence.")
                    except pynmea2.ParseError as e:
                        print(f"Could not parse line: {line}. Error: {e}")
    except serial.SerialException as e:
        print(f"Could not open serial port: {e}")
        return None

def get_location():
    port = 'COM8'  # Pas aan naar jouw poortnaam
    baudrate = 9600
    coordinates = get_gps_coordinates(port, baudrate)
    if coordinates:
        print(f'Coordinates: {coordinates}')
    else:
        print("No valid GPS data received.")

get_location()
