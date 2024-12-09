#!/bin/bash

ips=("185.131.204.20" "5.161.76.19" "80.77.4.60" "130.104.228.159")
methods=("UDP" "ICMP" "UDP-Paris" "ICMP-Paris" "TCP" "TCP-ACK")

# Crear el directorio "trace" si no existe
mkdir -p trace

# Iniciar captura de tráfico con tcpdump en la interfaz eth0
capture_file="traffic_capture_$(date +%Y%m%d%H%M%S).pcapng"
echo "Iniciando captura de tráfico en: $capture_file"
sudo tcpdump -i eth0 -w "$capture_file" &  # Captura tráfico en la interfaz eth0
tcpdump_pid=$!  # Obtener el PID del proceso tcpdump

# Asegurarse de detener tcpdump si el script es interrumpido
trap "echo 'Deteniendo captura de tráfico...'; sudo kill $tcpdump_pid" EXIT

# Ejecutar los comandos de scamper
for ip in "${ips[@]}"; do
  for method in "${methods[@]}"; do
    method_dir="trace/$method"
    mkdir -p "$method_dir"
    output_file="$method_dir/${ip}.txt"
    echo "sudo scamper -c 'trace -P $method' -i $ip"
    sudo scamper -c "trace -P $method" -i $ip | tee "$output_file"
    echo ""
  done
done

# Detener captura de tráfico al finalizar el script
echo "Deteniendo captura de tráfico..."
sudo kill $tcpdump_pid
trap - EXIT