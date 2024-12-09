import time
from ripe.atlas.cousteau import (
    AtlasSource,
    AtlasCreateRequest,
    Traceroute
)
import private

# Define las IPs destino y los IDs de las sondas
destinations = [
    {"ip": "185.131.204.20", "probe_id": 7344},
    {"ip": "5.161.76.19", "probe_id": 1000916},
    {"ip": "80.77.4.60", "probe_id": 7047},
    {"ip": "130.104.228.159", "probe_id": 6937}
]

# Define los protocolos a usar
protocols = ["UDP", "ICMP", "TCP"]

# Usa la API Key y la IP destino de private.py
api_key = private.api_key
target_ip = private.target_ip

# Obtener la hora actual en el formato deseado
current_time = time.strftime("%Y%m%d%H%M%S")

# Crea las mediciones
measurements = []
for destination in destinations:
    for protocol in protocols:
        traceroute = Traceroute(
            af=4,
            target=target_ip,
            description=f"Traceroute from {destination['probe_id']} to {target_ip} using {protocol}",
            protocol=protocol,
            resolve_on_probe=False
        )
        source = AtlasSource(
            type="probes",
            value=str(destination["probe_id"]),
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
            print(f"Error creating measurement from {destination['probe_id']} to {target_ip} using {protocol}")

print("Measurements created:", measurements)

print("Traceroute process completed.")