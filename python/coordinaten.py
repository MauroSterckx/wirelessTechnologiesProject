import json
import subprocess

def decrypt_tpms_data(data):
    """Decrypt and validate TPMS data."""
    try:
        # Example decryption/validation logic
        if "pressure_kPa" in data and data["pressure_kPa"] < 0:
            data["pressure_kPa"] = abs(data["pressure_kPa"])

        if "temperature_C" in data and data["temperature_C"] < -40:
            # Temperature below -40C is likely an error; set to a default value
            data["temperature_C"] = None

        return data
    except Exception as e:
        print(f"Error during decryption: {e}")
        return data

def run_rtl_433():
    """Start rtl_433 and process TPMS data."""
    try:
        # Start rtl_433 process with the specified command
        process = subprocess.Popen(
            [
                "rtl_433",
                "-f", "315M",  # TPMS frequency 315 MHz
                "-f", "433.92M",  # TPMS frequency 433.92 MHz
                "-Y", "autolevel",  # Enable auto level
                "-M", "protocol",  # Decode protocols
                "-C", "native",  # Output in native JSON format
                "-R", "147"  # TPMS-specific protocols
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,  # Ignore stderr
            text=True
        )
        print("Listening for TPMS signals...\n")

        # Process each line of JSON output
        for line in process.stdout:
            try:
                data = json.loads(line.strip())

                # Filter for TPMS-related data
                if data.get("model", "").lower().startswith("tpms"):
                    data = decrypt_tpms_data(data)
                    return {
                        "id": data.get("id"),
                        "model": data.get("model"),
                        "pressure_kPa": data.get("pressure_kPa"),
                        "temperature_C": data.get("temperature_C"),
                        "brand": data.get("brand"),
                        "manufacturer": data.get("manufacturer"),
                        "car": data.get("car")
                    }
            except json.JSONDecodeError:
                print(f"Could not decode line: {line.strip()}")
    except FileNotFoundError:
        print("rtl_433 is not installed or not found in PATH. Please install it and try again.")
        return None
    except KeyboardInterrupt:
        print("\nStopping rtl_433... Goodbye!")
        return None
    finally:
        process.terminate()
