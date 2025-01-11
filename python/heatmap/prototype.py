import requests
import folium
from folium.plugins import HeatMap
import json

# Definieer de URL om de data op te halen
url = 'https://wireless.maurosterckx.be/api/markers'

# Haal de data op
response = requests.get(url)
data = response.json()

# Haal de latitude en longitude gegevens eruit en sla ze op als tuples (lat, lon)
locations = [(marker['lat'], marker['lng']) for marker in data]

# Maak een folium map aan
m = folium.Map(location=[51.123957, 4.370547], zoom_start=13)

# Voeg een HeatMap laag toe aan de kaart
HeatMap(locations).add_to(m)

# Sla de kaart op in een HTML-bestand
m.save('heatmap.html')
