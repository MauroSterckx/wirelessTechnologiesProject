import requests

# Lijst van TPMS sensoren en hun compatibele automodellen
tpms_to_models = {
    "BOSCH F 026 C00 466": ["Volkswagen Golf (2012-2020)", "Audi A3 (2012-2018)"],
    "RIDEX 2232W0026": ["Ford Fiesta (2014-2020)", "Ford Focus (2014-2020)"],
    "RIDEX 2232W0102": ["BMW 3 Series (2012-2019)", "BMW 5 Series (2012-2019)"],
    "VDO S180211011Z": ["Hyundai Santa Fe (2013-2018)", "Kia Sorento (2013-2018)"],
    "Hamaton HTS-A69BM-S016": ["Mercedes-Benz C-Class (2014-2020)", "Mercedes-Benz E-Class (2014-2020)"],
    "SCHRADER 1210": ["Toyota Camry (2012-2017)", "Toyota Corolla (2012-2017)"],
    "SCHRADER 2200B-GO1": ["Honda Accord (2013-2017)", "Honda Civic (2013-2017)"],
    "SCHRADER 3049": ["Nissan Altima (2012-2018)", "Nissan Maxima (2012-2018)"],
    "PIERBURG 7.14060.13.0": ["Volkswagen Passat (2012-2018)", "Audi A4 (2012-2018)"],
    "HUF 73904101": ["BMW X5 (2013-2018)", "BMW X3 (2013-2018)"],
    "SKF VKRA 110039": ["Volvo XC90 (2015-2020)", "Volvo XC60 (2015-2020)"],
    "HUF 73907410": ["Porsche Cayenne (2011-2017)", "Porsche Panamera (2011-2017)"],
    "HELLA 6PP 358 139-461": ["Fiat 500 (2012-2019)", "Alfa Romeo Giulia (2015-2020)"],
    "HELLA 6PP 358 139-191": ["Renault Clio (2012-2019)", "Renault Megane (2012-2019)"],
    "HERTH+BUSS ELPARTS 70699434": ["Opel Astra (2015-2020)", "Opel Insignia (2015-2020)"]
}

# Haal de data op via de API
url = 'https://wireless.maurosterckx.be/api/markers'
response = requests.get(url)
data = response.json()

# Open een bestand om de resultaten weg te schrijven
with open("tpms_results.txt", "w") as file:
    # Maak een dictionary om het aantal voorkomen van elk automodel bij te houden
    model_count = {}

    # Koppel TPMS sensoren aan automodellen en schrijf de resultaten naar het bestand
    for marker in data:
        tpms_model = marker['tpms_data']['model']
        latitude = marker['lat']
        longitude = marker['lng']
        
        if tpms_model in tpms_to_models:
            file.write(f"TPMS Model: {tpms_model}\n")
            file.write("Compatible Automodellen:\n")
            
            for model in tpms_to_models[tpms_model]:
                file.write(f"- {model} (Locatie: {latitude}, {longitude})\n")
                if model in model_count:
                    model_count[model] += 1
                else:
                    model_count[model] = 1
                    
            file.write("\n")

    # Schrijf het aantal voorkomen van elk automodel naar het bestand
    file.write("Aantal voorkomens per automodel:\n")
    for model, count in model_count.items():
        file.write(f"{model}: {count} keer\n")

print("De resultaten zijn weggeschreven naar 'tpms_results.txt'.")
