import re

# Regular expression to match GPRMC sentences and extract latitude and longitude
gprmc_pattern = re.compile(r'\$GPRMC,\d{6},A,(\d{4}\.\d{5}),([NS]),(\d{5}\.\d{5}),([EW])')

# Function to process the GPRMC data and print coordinates
def extract_coordinates_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            match = gprmc_pattern.search(line)
            if match:
                lat = match.group(1)
                lat_dir = match.group(2)
                lon = match.group(3)
                lon_dir = match.group(4)
                
                # Convert to readable coordinates
                latitude = float(lat[:2]) + float(lat[2:])/60  # degrees + minutes/60
                if lat_dir == 'S':
                    latitude = -latitude  # South latitudes are negative
                
                longitude = float(lon[:3]) + float(lon[3:])/60  # degrees + minutes/60
                if lon_dir == 'W':
                    longitude = -longitude  # West longitudes are negative
                
                print(f"Latitude: {latitude:.5f}, Longitude: {longitude:.5f}")

# Example usage
file_path = r'data.txt'  # Replace with your actual file path
extract_coordinates_from_file(file_path)
