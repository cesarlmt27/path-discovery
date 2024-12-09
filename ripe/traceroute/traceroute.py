import subprocess
import time
import threading
import os
import getpass
from ripe.atlas.cousteau import (
    AtlasSource,
    AtlasCreateRequest,
    Traceroute
)
import private

# Define las IPs destino
destinations = [
    {"ip": "185.131.204.20"},
    {"ip": "5.161.76.19"},
    {"ip": "80.77.4.60"},
    {"ip": "130.104.228.159"}
]

# Define los protocolos a usar
protocols = ["UDP", "ICMP", "TCP"]

# Usa la API Key y el ID de la sonda de private.py
api_key = private.api_key
probe_id = private.probe_id

# Obtener la hora actual en el formato deseado
current_time = time.strftime("%Y%m%d%H%M%S")

# Nombre del archivo de captura
capture_filename = f"traffic_capture_{current_time}.pcapng"
capture_filepath = os.path.abspath(capture_filename)

# Solicitar la contraseña de sudo
sudo_password = getpass.getpass(prompt="Enter your sudo password: ")

# Iniciar captura con tcpdump
tcpdump_process = subprocess.Popen(
    ["sudo", "-S", "tcpdump", "-i", "docker0", "-w", capture_filepath],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

# Pasar la contraseña a sudo
tcpdump_process.stdin.write(sudo_password.encode() + b'\n')
tcpdump_process.stdin.flush()

# Crea las mediciones
measurements = []
for destination in destinations:
    for protocol in protocols:
        traceroute = Traceroute(
            af=4,
            target=destination["ip"],
            description=f"Traceroute to {destination['ip']} using {protocol}",
            protocol=protocol,
            resolve_on_probe=False
        )
        source = AtlasSource(
            type="probes",
            value=str(probe_id),
            requested=1
        )
        atlas_request = AtlasCreateRequest(
            start_time=None,
            key=api_key,
            measurements=[traceroute],
            sources=[source],
            is_oneoff=True
        )
        is_success, response = atlas_request.create()
        if is_success:
            measurements.append(response)
        else:
            print(f"Error creating measurement for {destination['ip']} using {protocol}")

print("Measurements created:", measurements)

# Esperar a que el usuario presione una tecla para finalizar la captura con tcpdump
def wait_for_keypress():
    input("Press Enter to stop tcpdump...")

keypress_thread = threading.Thread(target=wait_for_keypress)
keypress_thread.start()
keypress_thread.join()

# Finalizar captura con tcpdump
tcpdump_process.terminate()
tcpdump_process.wait()

print("TCPDump capture completed.")