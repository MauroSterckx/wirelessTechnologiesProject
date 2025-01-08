import json
import subprocess

def decrypt_tpms_data(data):
    """Decrypt and validate TPMS data."""
    try:
        # Simpele validatielogica
        if "pressure_kPa" in data and data["pressure_kPa"] < 0:
            data["pressure_kPa"] = abs(data["pressure_kPa"])

        if "temperature_C" in data and data["temperature_C"] < -40:
            # Temperaturen onder -40C zijn waarschijnlijk onjuist
            data["temperature_C"] = None

        return data
    except Exception as e:
        print(f"Error during decryption: {e}")
        return data

def run_rtl_433():
    """Start rtl_433 en verwerk TPMS-data."""
    process = None
    try:
        # Voer rtl_433 uit met juiste parameters
        process = subprocess.Popen(
            [
                r"C:\rtl_433\rtl_433.exe",  # Correct pad naar rtl_433
                "-f", "433.92M",           # Frequentie 433.92 MHz
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,  # Negeer stderr
            text=True
        )
        print("Listening for TPMS signals...\n")

        # Verwerk de uitvoerregel voor regel
        for line in process.stdout:
            try:
                data = json.loads(line.strip())

                # Filter voor TPMS-gerelateerde data
                if "model" in data and "tpms" in data["model"].lower():
                    data = decrypt_tpms_data(data)
                    print("Received TPMS data:")
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
