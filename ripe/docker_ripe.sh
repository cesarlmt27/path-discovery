#!/bin/bash

docker run --detach --restart=always \
	--log-driver json-file --log-opt max-size=10m \
	--cpus=1 --memory=64m --memory-reservation=64m \
	--cap-drop=ALL --cap-add=CHOWN --cap-add=SETUID --cap-add=SETGID --cap-add=DAC_OVERRIDE --cap-add=NET_RAW \
	-v /var/atlas-probe/etc:/var/atlas-probe/etc \
	-v /var/atlas-probe/status:/var/atlas-probe/status \
	-e RXTXRPT=yes \
	--name ripe-atlas --hostname "$(hostname --fqdn)" \
	jamesits/ripe-atlas:latest