import csv
import os
import requests

# Ruta del archivo CSV de entrada
input_file_path = 'trace/UDP-Paris/80.77.4.60.csv'

# Obtener el nombre del archivo original sin la extensión
input_file_name = os.path.basename(input_file_path)
file_name_without_ext = os.path.splitext(input_file_name)[0]

# Crear el nombre del archivo de salida
output_file_name = f"{file_name_without_ext}_metadata.csv"
output_file_path = os.path.join(os.getcwd(), output_file_name)

# Función para obtener el nombre del país y la ciudad desde la API ip2location.io
def get_location_data(ip):
    try:
        response = requests.get(f'https://api.ip2location.io/?ip={ip}')
        response.raise_for_status()
        data = response.json()
        country_name = data.get('country_name', '')
        city_name = data.get('city_name', '')
        return country_name, city_name
    except requests.RequestException:
        return '', ''

# Función para obtener el ISP desde la API iplocation.net
def get_isp(ip):
    try:
        response = requests.get(f'https://api.iplocation.net/?ip={ip}')
        response.raise_for_status()
        data = response.json()
        isp = data.get('isp', '')
        return isp
    except requests.RequestException:
        return ''

# Leer el archivo CSV de entrada
with open(input_file_path, mode='r', newline='') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Omitir la primera fila después del encabezado
if len(rows) > 0:
    rows = rows[1:]

# Preparar los datos para el archivo CSV de salida
output_rows = []
hop = 1
for row in rows:
    ip = row['IP']
    as_number = row['AS']
    if ip != '*':
        country_name, city_name = get_location_data(ip)
        isp = get_isp(ip)
    else:
        country_name, city_name, isp = '', '', ''
    output_rows.append({
        'IP': ip,
        'Hop': hop,
        'AS': as_number,
        'Country': country_name,
        'City': city_name,
        'ISP': isp
    })
    hop += 1

# Escribir el archivo CSV de salida
with open(output_file_path, mode='w', newline='') as outfile:
    fieldnames = ['IP', 'Hop', 'AS', 'Country', 'City', 'ISP']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(output_rows)

print(f"Archivo procesado guardado en: {output_file_path}")