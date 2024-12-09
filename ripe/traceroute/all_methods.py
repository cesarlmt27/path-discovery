import os
import csv
from collections import defaultdict

# Directorio raíz
root_dir = 'traceroute'
output_dir = 'compare_methods'

# Crear el directorio de salida si no existe
os.makedirs(output_dir, exist_ok=True)

# Diccionario para almacenar los datos
data = defaultdict(lambda: defaultdict(list))

# Recorrer todos los subdirectorios y archivos
for subdir, _, files in os.walk(root_dir):
    method = os.path.basename(subdir)
    for file in files:
        if file.endswith('.csv'):
            file_path = os.path.join(subdir, file)
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    ip = row['IP']
                    data[file][method].append(ip)

# Crear archivos CSV combinados por cada archivo original
for file, methods in data.items():
    output_file = os.path.join(output_dir, f'{os.path.splitext(file)[0]}_hops.csv')
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        # Obtener todos los métodos
        all_methods = sorted(methods.keys())
        
        # Escribir encabezado
        writer.writerow(all_methods)
        
        # Escribir datos
        max_len = max(len(methods[method]) for method in all_methods)
        for i in range(max_len):
            row = []
            for method in all_methods:
                if i < len(methods[method]):
                    row.append(methods[method][i])
                else:
                    row.append('')
            writer.writerow(row)

print("Archivos combinados creados en el directorio 'compare_methods'.")