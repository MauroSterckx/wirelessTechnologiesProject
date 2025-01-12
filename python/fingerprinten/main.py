import requests

# Sensor-naar-auto mapping
sensor_to_cars = {
    "Hamaton EU-Pro Hybrid 3.5 Bar": ["Audi A3 (2014-2020)", "Volkswagen Golf VII (2013-2020)"],
    "Schrader EZ-sensor 33500": ["Ford Focus (2015-2021)", "BMW 3 Serie (F30, 2012-2019)"],
    "Pacific TPMS Sensor": ["Toyota Prius (2010-2015)", "Lexus RX (2012-2015)"],
    "VDO Redi-Sensor SE10001HP": ["Mercedes-Benz C-Klasse (2015-2020)", "BMW X5 (2013-2018)"],
    "Continental VDO TG1C": ["Volkswagen Passat (2015-2021)", "Audi Q5 (2017-2021)"]
}

def fetch_sensor_data():
    url = "https://wireless.maurosterckx.be/api/markers"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def match_sensors_to_cars(sensor_data):
    if not sensor_data:
        print("No data to process.")
        return

    for marker in sensor_data.get('data', []):
        sensor_model = marker.get('tpms_data', {}).get('model', 'Onbekend')
        matched_cars = sensor_to_cars.get(sensor_model, ["Onbekend model"])
        print(f"Sensor ID: {marker.get('tpms_data', {}).get('id', 'Onbekend')} => Compatibele auto's: {', '.join(matched_cars)}")

def main():
    data = fetch_sensor_data()
    match_sensors_to_cars(data)

if __name__ == "__main__":
    main()
