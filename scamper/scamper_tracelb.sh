#!/bin/bash

ips=("185.131.204.20" "5.161.76.19" "80.77.4.60" "130.104.228.159")

# Crear el directorio "tracelb" si no existe
mkdir -p tracelb

# Ejecutar los comandos de scamper
for ip in "${ips[@]}"; do
  output_file="tracelb/${ip}.txt"
  echo "sudo scamper -c 'tracelb' -i $ip"
  sudo scamper -c "tracelb" -i $ip | tee "$output_file"
  echo ""
done