import requests
import json

# Bestandspad naar de JSON-bestand
json_file_path = 'alle_data.json'

# Lezen van de JSON-data uit het bestand
with open(json_file_path, 'r') as file:
    data = json.load(file)

# API-endpoint
url = 'https://wireless.maurosterckx.be/api/markers'

# Headers
headers = {
    'Content-Type': 'application/json'
}

# Verstuur elk item afzonderlijk
for item in data:
    response = requests.post(url, headers=headers, json=item)
    
    # Debug informatie om de response te bekijken
    print(f"Verstuurd item: {item['name']}")
    print("Status Code:", response.status_code)
    print("Response:", response.text)

    # Controleer de response status
    if response.status_code == 200:
        print(f'Data van {item["name"]} succesvol verzonden naar de API.')
    else:
        print(f'Niet gelukt om data van {item["name"]} te verzenden. Statuscode: {response.status_code}')
