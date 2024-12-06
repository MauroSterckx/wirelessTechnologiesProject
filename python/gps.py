import socket

# Gebruik 0.0.0.0 om op alle interfaces te luisteren
host = "0.0.0.0"
port = 11123

def start_server():
    print(f"Listening for GPS data on {host}:{port}...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((host, port))
        while True:
            data, addr = server.recvfrom(1024)  # Data ontvangen
            decoded_data = data.decode("utf-8").strip()
            print(f"Received from {addr}: {decoded_data}")

if __name__ == "__main__":
    start_server()
