import re
from collections import defaultdict
from datetime import datetime

# Sample data as a multi-line string
raw_data = """
---

time : 2024-12-06 13:26:16
model : Abarth-124Spider type : TPMS id : c15a6b8e
flags : 60 Pressure : 276 kPa Temperature: 14 C
status : 11 Integrity : CHECKSUM

---

time : 2024-12-06 13:26:16
model : Renault-0435R type : TPMS id : c15a6b
flags : 8e Pressure : 128.0 kPa Temperature: 150 C
Centrifugal Acceleration: 320 m/s2 mic : CRC
has_tick : 1 tick : 29

---

time : 2024-12-06 13:26:16
model : Abarth-124Spider type : TPMS id : c15a6b8e
flags : 60 Pressure : 276 kPa Temperature: 14 C
status : 11 Integrity : CHECKSUM

---

time : 2024-12-06 13:26:16
model : Renault-0435R type : TPMS id : c15a6b
flags : 8e Pressure : 128.0 kPa Temperature: 150 C
Centrifugal Acceleration: 320 m/s2 mic : CRC

---

time : 2024-12-06 13:33:11
model : Abarth-124Spider type : TPMS id : c15a6b9c
flags : 60 Pressure : 264 kPa Temperature: 16 C
status : 7 Integrity : CHECKSUM

---

time : 2024-12-06 13:33:11
model : Truck type : TPMS id : 15a6b9c6
wheel : 11 Pressure : 1056 kPa Temperature: 127 C
State? : c Flags? : f Integrity : CHECKSUM

---

time : 2024-12-06 13:32:41
model : Abarth-124Spider type : TPMS id : c15a6b6f
flags : 60 Pressure : 269 kPa Temperature: 16 C
status : 13 Integrity : CHECKSUM
\*\*\* Saving signal to file g001_433.92M_1024k.cu8 (43573 samples, 131072 bytes)

---

time : 2024-12-06 13:32:42
model : Abarth-124Spider type : TPMS id : c15a6b6f
flags : 60 Pressure : 269 kPa Temperature: 16 C
status : 13 Integrity : CHECKSUM

---

time : 2024-12-06 13:32:42
model : Truck type : TPMS id : 15a6b6f6
wheel : 12 Pressure : 1056 kPa Temperature: 215 C
State? : c Flags? : 3 Integrity : CHECKSUM
\*\*\* Saving signal to file g002_433.92M_1024k.cu8 (158706 samples, 393216 bytes)
Estimated noise level is -38.2 dB, adjusting minimum detection level to -35.2 dB
Estimated noise level is -37.1 dB, adjusting minimum detection level to -34.1 dB
Current noise level -38.8 dB, estimated noise -37.6 dB
Estimated noise level is -38.3 dB, adjusting minimum detection level to -35.3 dB
Estimated noise level is -39.3 dB, adjusting minimum detection level to -36.3 dB

---

time : 2024-12-06 13:32:58
model : Abarth-124Spider type : TPMS id : c15a6b6f
flags : 60 Pressure : 269 kPa Temperature: 16 C
status : 13 Integrity : CHECKSUM
"""

# Regex patterns for extracting data
entry_pattern = re.compile(r"""time : (?P<time>\S+ \S+)\nmodel : (?P<model>\S+(?:-\S+)?) type : TPMS id : (?P<id>\S+)\n.*?Pressure : (?P<pressure>\d+(?:\.\d+)?) kPa Temperature: (?P<temperature>\d+) C.*?(?=\n\n|\Z)""", re.DOTALL)

# Parse the data into a structured format
def parse_data(raw_data):
    entries = []
    for match in entry_pattern.finditer(raw_data):
        entry = {
            "time": datetime.strptime(match.group("time"), "%Y-%m-%d %H:%M:%S"),
            "model": match.group("model"),
            "id": match.group("id"),
            "pressure": float(match.group("pressure")),
            "temperature": int(match.group("temperature")),
        }
        entries.append(entry)
    return entries

# Group data by car ID
def group_by_car(entries):
    cars = defaultdict(list)
    for entry in entries:
        cars[entry["id"]].append(entry)
    return cars

# Generate fingerprints for each car
def fingerprint_cars(car_data):
    fingerprints = {}
    for car_id, readings in car_data.items():
        model = readings[0]["model"]
        pressures = [reading["pressure"] for reading in readings]
        temperatures = [reading["temperature"] for reading in readings]
        avg_pressure = sum(pressures) / len(pressures)
        avg_temperature = sum(temperatures) / len(temperatures)

        fingerprints[car_id] = {
            "model": model,
            "average_pressure": avg_pressure,
            "average_temperature": avg_temperature,
            "readings_count": len(readings),
        }
    return fingerprints

# Main script execution
def main():
    entries = parse_data(raw_data)
    car_data = group_by_car(entries)
    fingerprints = fingerprint_cars(car_data)

    print("Car Fingerprints:")
    for car_id, fingerprint in fingerprints.items():
        print(f"ID: {car_id}")
        print(f"  Model: {fingerprint['model']}")
        print(f"  Average Pressure: {fingerprint['average_pressure']:.2f} kPa")
        print(f"  Average Temperature: {fingerprint['average_temperature']:.2f} C")
        print(f"  Number of Readings: {fingerprint['readings_count']}")
        print()

if __name__ == "__main__":
    main()
