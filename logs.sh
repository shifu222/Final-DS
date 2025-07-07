# !/bin/bash

#si hay un error se detiene
set -e

#crea el directorio de logs
mkdir -p logs

#la ruta del los logs
LOG_FILE="logs/EF.log"

#vacia los logs 
> "$LOG_FILE"


#ejecuto docker build
echo "Ejecutando docker build"
docker build -t product-service:latest ./src/serviceB/. >> "$LOG_FILE"

docker build -t user-service:latest ./src/serviceA/. >> "$LOG_FILE"

