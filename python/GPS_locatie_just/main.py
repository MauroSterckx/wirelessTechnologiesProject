import json
from auto_fingerprint import run_rtl_433
from gps_glonass import get_gps_coordinates

def get_location():
    """Haalt GPS-coördinaten op."""
    port = 'COM8'  # Pas aan naar jouw poortnaam
    baudrate = 9600
    coordinates = get_gps_coordinates(port, baudrate)
    if coordinates:
        return coordinates
    else:
        print("No valid GPS data received.")
        return {"lat": None, "lng": None}

def main():
    print("Starting to listen for TPMS signals and GPS locations...\n")
    
    while True:
        # Roep de TPMS-functie aan en wacht op een signaal
        tpms_data = run_rtl_433()
        if tpms_data:
            print("TPMS signal detected!")
            
            # Roep de GPS-functie aan na het detecteren van een signaal
            gps_data = get_location()

            # Combineer de gegevens
            combined_data = {
                "name": "Schelle Marker",
                "lat": gps_data.get("lat"),
                "lng": gps_data.get("lng"),
                "tpms_data": tpms_data
            }

            # Retourneer de gecombineerde gegevens
            print("\nCombined Data:")
            print(json.dumps(combined_data, indent=4))
        else:
            print("No TPMS data detected. Retrying...\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram stopped by user. Goodbye!")
