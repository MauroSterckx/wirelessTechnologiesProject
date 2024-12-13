import numpy as np
import pyhackrf
import time

# Function to load the .cu8 file (assuming it's a raw I/Q data file)
def load_cu8_data(filename):
    data = np.fromfile(filename, dtype=np.int8)
    # Ensure the data is in pairs (I, Q) format
    if len(data) % 2 != 0:
        print("Error: Data length is not even!")
        return None
    # Reshape data to (N, 2), where N is the number of samples
    iq_data = data.reshape(-1, 2)
    return iq_data

# Function to initialize HackRF
def initialize_hackrf(frequency=915e6, sample_rate=10e6):
    hackrf_device = pyhackrf.HackRF()  # Initialize HackRF
    hackrf_device.setup()
    hackrf_device.set_freq(frequency)  # Set frequency (e.g., 915 MHz)
    hackrf_device.set_sample_rate(sample_rate)  # Set sample rate (e.g., 10 MHz)
    hackrf_device.set_txvga_gain(20)  # Adjust Tx gain if needed
    return hackrf_device

# Function to transmit the data through HackRF
def transmit_data(hackrf_device, iq_data):
    try:
        for i in range(0, len(iq_data), 1024):  # Transmit in chunks
            # Create a chunk of data to send
            chunk = iq_data[i:i+1024]
            # Send data as a byte stream
            hackrf_device.send_data(chunk.tobytes())
            time.sleep(0.1)  # Add a small delay between transmissions
    except Exception as e:
        print(f"Error during transmission: {e}")

# Main function to load data and transmit
def main():
    # Specify the file path of the encrypted .cu8 file
    filename = "data.cu8"
    print(f"Loading .cu8 data from {filename}...")
    
    iq_data = load_cu8_data(filename)
    if iq_data is None:
        print("Failed to load data.")
        return
    
    print(f"Loaded {len(iq_data)} samples from the .cu8 file.")

    # Initialize HackRF
    print("Initializing HackRF...")
    hackrf_device = initialize_hackrf()

    # Start transmitting the data
    print("Starting transmission...")
    transmit_data(hackrf_device, iq_data)

    # Close HackRF when done
    hackrf_device.close()
    print("Transmission completed. HackRF closed.")

if __name__ == "__main__":
    main()
