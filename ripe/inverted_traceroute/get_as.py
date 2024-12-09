import os
import csv
import requests
from bs4 import BeautifulSoup
from ripe.atlas.cousteau import AtlasResultsRequest
import private

# Usa la API Key de private.py
api_key = private.api_key

# IDs de las mediciones realizadas (proporcionados manualmente)
measurement_ids = [
    84265937,
    84265953,
    84265954,
    84265955,
    84265956,
    84265957,
    84265958,
    84265959,
    84265960,
    84265961,
    84265962,
    84265963
]

# Obtener resultados de una medición
def get_measurement_results(measurement_id):
    kwargs = {
        "msm_id": measurement_id,
        "key": api_key
    }
    is_success, results = AtlasResultsRequest(**kwargs).create()
    if is_success:
        return results
    else:
        print(f"Error fetching results for measurement ID {measurement_id}")
        return None

# Obtener información de IP desde bgp.he.net
def get_ip_info(ip):
    if ip == '*':
        return None, None
    try:
        url = f"https://bgp.he.net/ip/{ip}#_ipinfo"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        ip_info_div = soup.find('div', {'id': 'ipinfo', 'class': 'tabdata'})
        if ip_info_div:
            table = ip_info_div.find('table')
            if table:
                rows = table.find_all('tr')
                for row in rows[2:]:  # Saltar las dos primeras filas de encabezado
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        asn = cols[0].text.strip()
                        description = cols[2].text.strip()
                        return asn, description
    except Exception as e:
        print(f"Error procesando IP {ip}: {e}")
    return None, None

# Procesar resultados y guardar en archivos CSV
def process_and_save_results(results):
    for result in results:
        src_addr = result['src_addr']
        protocol = result['proto']
        hops = result['result']

        # Crear directorio si no existe
        directory = os.path.join('measurements', protocol)
        os.makedirs(directory, exist_ok=True)

        # Nombre del archivo CSV
        csv_filename = os.path.join(directory, f"{src_addr}.csv")

        # Usar una lista para mantener el orden y un conjunto para evitar duplicados
        ordered_ips = []

        # Escribir resultados en el archivo CSV
        with open(csv_filename, mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['IP', 'AS', 'Description'])

            for hop in hops:
                if hop['result']:
                    first_result = hop['result'][0]
                    ip = first_result.get('from', '*')
                    ordered_ips.append(ip)

            for ip in ordered_ips:
                asn, description = get_ip_info(ip)
                csv_writer.writerow([ip, asn if asn else '', description if description else ''])

# Obtener resultados para cada medición
for measurement_id in measurement_ids:
    results = get_measurement_results(measurement_id)
    if results:
        process_and_save_results(results)