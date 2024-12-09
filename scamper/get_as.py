import requests
from bs4 import BeautifulSoup
import csv
import re
import glob

def extract_ips_from_file(file_path):
    ips = []
    with open(file_path, 'r') as file:
        for line in file:
            # Buscar coincidencias de IPs o asteriscos en cada línea
            match = re.search(r'(\d+\.\d+\.\d+\.\d+|\*)', line)
            if match:
                ips.append(match.group(1))
    return ips

def get_ip_info(ip):
    # Si la IP es un asterisco, retornar valores vacíos
    if ip == '*':
        return None, None
    try:
        # Realizar una solicitud GET a la URL de bgp.he.net para obtener información de la IP
        url = f"https://bgp.he.net/ip/{ip}#_ipinfo"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Buscar el div con la información de la IP
        ip_info_div = soup.find('div', {'id': 'ipinfo', 'class': 'tabdata'})
        if ip_info_div:
            # Buscar la tabla dentro del div
            table = ip_info_div.find('table')
            if table:
                # Obtener todas las filas de la tabla
                rows = table.find_all('tr')
                for row in rows[2:]:  # Saltar las dos primeras filas de encabezado
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        # Extraer el ASN y la descripción de las columnas correspondientes
                        asn = cols[0].text.strip()
                        description = cols[2].text.strip()
                        return asn, description
    except Exception as e:
        print(f"Error procesando IP {ip}: {e}")
    return None, None

def write_to_csv(file_path, data):
    # Generar la ruta del archivo CSV reemplazando la extensión .txt por .csv
    csv_file_path = file_path.replace('.txt', '.csv')
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['IP', 'AS', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Escribir cada fila de datos en el archivo CSV
        for row in data:
            writer.writerow(row)

def process_file(file_path):
    # Extraer las IPs del archivo de texto
    ips = extract_ips_from_file(file_path)
    data = []
    for ip in ips:
        print(f"Procesando IP: {ip}")
        # Obtener la información de la IP
        asn, description = get_ip_info(ip)
        print(f"ASN: {asn}, Description: {description}")
        # Agregar la información de la IP a la lista de datos
        data.append({'IP': ip, 'AS': asn if asn else '', 'Description': description if description else ''})
    # Escribir los datos en un archivo CSV
    write_to_csv(file_path, data)

def main():
    # Buscar todos los archivos .txt en el directorio trace y sus subdirectorios
    txt_files = glob.glob('trace/**/*.txt', recursive=True)
    for file_path in txt_files:
        print(f"Procesando archivo: {file_path}")
        # Procesar cada archivo de texto encontrado
        process_file(file_path)

if __name__ == "__main__":
    main()