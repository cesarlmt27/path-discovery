# Path discovery
Este repositorio contiene scripts implementados para realizar trazado de rutas y caracterización de tráfico en redes. Se basa en el uso de herramientas como **[Scamper](https://www.caida.org/catalog/software/scamper/)**, **[tcpdump](https://www.tcpdump.org/)**, y mediciones realizadas con **[RIPE Atlas](https://atlas.ripe.net/)**; además de consultas a APIs externas para obtención de metadatos.

El objetivo principal es estudiar y caracterizar el comportamiento de diferentes protocolos y métodos de traceroute, analizando su respuesta en distintas arquitecturas de redes.


## **Trazado de rutas (Traceroute)**
Se implementan los métodos *UDP*, *ICMP*, *UDP-Paris*, *ICMP-Paris*, *TCP* y *TCP-ACK* para analizar la ruta hacia destinos específicos.


## **Mediciones con RIPE Atlas**
Se incluye el uso de mediciones realizadas con sondas de **RIPE Atlas**, que permiten comparar rutas obtenidas con RIPE Atlas frente a las de herramientas locales como Scamper. Estas mediciones aprovechan la red global de sondas para obtener datos desde distintas regiones geográficas.


## **Captura de tráfico**
Se realizan capturas de tráfico mediante **tcpdump** durante la ejecución de los trazados de rutas. Estas capturas permiten:
- Analizar los encabezados de los paquetes para caracterizar flujos.
- Visualizar detalles como puertos, TTL, tamaños de payload, y secuencias de paquetes.
- Generar archivos `.pcapng` para su análisis posterior con herramientas como Wireshark.


## **Obtención de Sistemas Autónomos (AS)**
Se realizan consultas a [Hurricane Electric BGP Toolkit](https://bgp.he.net/) para obtener el AS asociado a una IP.


## **Obtención de metadatos de IP**
Se obtienen los metadatos país, ciudad y proveedor de servicios de internet, de las APIs [IP2Location](https://www.ip2location.io/) y [IPLocation](https://www.iplocation.net/).


## Referencias
- Center for Applied Internet Data Analysis. (2024a). Scamper. Retrieved from https://www.caida.org/catalog/software/scamper/
- Center for Applied Internet Data Analysis. (2024b). Scamper - BSD General Commands Manual. Retrieved from https://www.caida.org/catalog/software/scamper/man/scamper.1.pdf
- Jamesits. (2024). RIPE Atlas Docker Image. Retrieved from https://github.com/Jamesits/docker-ripe-atlas
- Ripe NCC. (2024). RIPE Atlas Documentation. Retrieved from https://atlas.ripe.net/docs/
- RIPE NCC. (2023). RIPE Atlas Cousteau. Retrieved from https://ripe-atlas-cousteau.readthedocs.io/