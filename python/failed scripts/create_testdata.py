import numpy as np

# Parameters for the signal
sample_rate = 1024000  # 1.024 MHz
frequency = 915000000  # 915 MHz
duration = 1  # 1 second
amplitude = 127  # Maximum amplitude for 8-bit values

# Generate time vector
t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)

# Generate I/Q signal (simple sine wave)
iq_signal = amplitude * np.cos(2 * np.pi * frequency * t)  # I component (cosine)
iq_signal = iq_signal.astype(np.int8)  # Convert to 8-bit integer values

# Save the signal as a .bin file
iq_signal.tofile("test_signal.bin")
