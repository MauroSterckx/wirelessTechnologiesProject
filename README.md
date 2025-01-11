# wirelessTechnologiesProject

AP Hogeschool Wireless Technologies Project

## Teamleden

- Mauro Sterckx
- Gerben van de Velde
- Yenthe Van den Eynden
- Klaas Mouws

## Website github repo
Voor CI/CD pipeline mogelijkheden werd de website die we gemaakt hebben voor dit project in een eigen github repository verdeeld:
[Github repo link](https://github.com/MauroSterckx/WirelessWebsite.git)

## Timetable

### 24Nov - 1 Dec

#### Mauro

- HackRF gebruikt
- SDR gebruikt
- SDR++ geinstalleerd
- RTL 433 geinstalleerd
  - SoapySDR voor hackRF te kunnen gebruiken
    - Geen data gekregen op rtl 433, op SDR++ wel waargenomen
  - SDR (zonder SoapySDR)
    - Geen data gekregen op rtl 433, op SDR++ wel waargenomen
  - Vermoeden dat er iets niet correct verloopt bij gebruikt met rtl433, kan deze wel iets waarnemen?
    - Volgende keer proberen met SDR++ te luisteren en dan RTL433 via TCP naar SDR++ te verbinden

#### Gerben

- SDR gebruikt
- AIRSPY SDR geïnstalleerd
- RTL 433 geïnstalleerd
  - De SDR laten scannen op 433 maar kreeg geen signalen
    - Er achter gekomen dat de auto dit enkel zend als er grote verschillen zijn in druk of als de auto aan het rijden is
- python script gebruikt om de MQTT relay te monitoren

#### Yenthe

- mee opgezocht hoe HackRF te gebruiken met rtl 433

#### Klaas

- DragonOS testen
- testen met AIRSPY SDR + RTL-SDR auto signalen ontvangen

### 2 - 8 Dec

#### Mauro

- SDR++ server gebruikt en rtl433 laten connecten naar de SDR++ server, dit werkte. Nog steeds geen data waargenomen
- Data wordt wel waargenomen, maar heb ontdekt dat er problemen zijn met het decoden. Dankzij -vvv flag te gebruiken zie ik decoding errors
- Example config file van 433 github repo geprobeert te gebruiken, geeft errors!

### Mauro & Gerben

- Wardriven met auto
- TPMS gemeten via RTL 433, van eigen wagen, andere wagens en weerstations
- GPS server opgezet via telefoon
- GPS locaties opvangen en python script dat het noteert in long en lat
- encrypted data opgeslagen voor terug uit te zenden, decrypted om mogelijk het in beeld te brengen op kaart

### Yenthe

- HackRFone getest
  - data kunnen versturen
- tests met DragonOS

### Klaas

- SDR testen
- Opzoeken NMEA gps module
- Testen NMEA gps module python
- Signalen draadloos stopcontact ontvangen en analyseren

#### voorlopige taakverdeling:

#### Iedereen:

-Eerste werkende scans binnenhalen en kunnen decoderen via rtl 433
-testen met eigen auto

-Auto's proberen fingerprinten

### 9 - 15 Dec

#### Mauro

- Website:
  - API & Frontend basics gemaakt
- HackRF
  - Testdata verzonden
  - CU8 naar .bin proberen om te zetten

#### Gerben

- Python scripts:
  - CU8 & Bin generators
  - RTL op SDR install

### Klaas
- Python script dat GPS locatie ophaald van een Glonas GPS module
- Telkens wanneer auto wordt gefingerprint treed dit script in werking zodat de gps locatie kan worden bevestigd
#### voorlopige taakverdeling

#### Yenthe & Klaas

- python script maken dat GPS locatie en de RTL 433 scan samen uitvoert, zodat we auto's kunnen koppelen aan locatie

#### Mauro & Gerben

- API maken voor de locatie en RTL 433 van auto op te slaan
- encrypted data proberen uitzenden via de HackOneRF om auto te simuleren


### 16 - 22 Dec

#### Mauro

- .bin file proberen uitzenden via HackRF One
- zelf .bin file maken
- auto fingerprinten

#### Gerben

- auto fingerprinten
- opnieuw gaan wardriven voor meer informatie en .bin files

### Klaas

- Script geschreven dat telkens wanneer er een auto gefingerprint wordt, de gps glonass module in werking treedt en de exacte gps locatie ophaalt
- Getest

#### voorlopige taakverdeling

iedereen:
- .bin file kunnen uitzenden waardoor auto gesimuleerd wordt
- finale python script schrijven
