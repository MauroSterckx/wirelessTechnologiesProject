import json
import subprocess
import serial
import pynmea2
import time
import os

# Functie om NMEA latitude/longitude om te zetten naar decimale graden
def convert_to_decimal(degrees_minutes, direction):
    if not degrees_minutes or not direction:
        raise ValueError("Invalid NMEA data: degrees_minutes or direction is empty.")
    
    degrees = int(float(degrees_minutes) // 100)
    minutes = float(degrees_minutes) % 100
    decimal = degrees + (minutes / 60)
    
    if direction in ['S', 'W']:
        decimal = -decimal
    return round(decimal, 6)

# Functie om de eerste NMEA-zin met locatiegegevens te lezen
def get_gps_coordinates(port, baudrate=9600, timeout=1):
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as stream:
            print(f"Listening for NMEA data on {port} at {baudrate} baud...")
            start_time = time.time()
            while True:
                line = stream.readline().decode('ascii', errors='ignore').strip()
                if line.startswith('$'):
                    try:
                        msg = pynmea2.parse(line)
                        if hasattr(msg, 'lat') and hasattr(msg, 'lon'):
                            if msg.lat and msg.lon:
                                lat = convert_to_decimal(msg.lat, msg.lat_dir)
                                lng = convert_to_decimal(msg.lon, msg.lon_dir)
                                return {"lat": lat, "lng": lng}
                    except pynmea2.ParseError as e:
                        print(f"Could not parse line: {line}. Error: {e}")
                if time.time() - start_time > timeout:
                    print("Timeout reached. No valid GPS data found.")
                    break
        return {"lat": 0, "lng": 0}  # Default locatie als geen GPS-data wordt ontvangen
    except serial.SerialException as e:
        print(f"Could not open serial port: {e}")
        return {"lat": 0, "lng": 0}  # Return default location if GPS fails

# Functie om TPMS data te decrypteren en te valideren
def decrypt_tpms_data(data):
    try:
        if "pressure_kPa" in data and data["pressure_kPa"] < 0:
            data["pressure_kPa"] = abs(data["pressure_kPa"])

        if "temperature_C" in data and data["temperature_C"] < -40:
            data["temperature_C"] = None

        return data
    except Exception as e:
        print(f"Error during decryption: {e}")
        return data

def run_rtl_433():
    """Start rtl_433 en verwerk TPMS-data met GPS-coördinaten."""
    process = None
    try:
        process = subprocess.Popen(
            [
                r"C:\rtl_433\rtl_433.exe",
                "-f", "433.92M",  # Frequentie 433.92 MHz
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        print("Listening for TPMS signals...\n")

        # Verkrijg de GPS-coördinaten bij het opstarten
        gps_coordinates = get_gps_coordinates('COM5')  # Pas aan naar de juiste poorthrteh
        print(f"Initial GPS Coordinates: {gps_coordinates}")

        # Verwerk de uitvoerregel voor regel28727
        for line in process.stdout:
            try:
                data = json.loads(line.strip())

                if "model" in data and "tpms" in data["model"].lower():
                    data = decrypt_tpms_data(data)

                    # Voeg GPS-coördinaten toe aan de TPMS-data
                    data["gps_coordinates"] = gps_coordinates
                    
                    # Print de gecombineerde data
                    print("Received TPMS data with GPS coordinates:")
                    print(json.dumps(data, indent=4))

            except json.JSONDecodeError:
                print(f"Could not decode line: {line.strip()}")
    except FileNotFoundError:
        print("rtl_433 is not found. Please check the installation and path.")
    except KeyboardInterrupt:
        print("\nStopping rtl_433... Goodbye!")
    finally:
        if process:
            process.terminate()

if __name__ == "__main__":
    run_rtl_433()
