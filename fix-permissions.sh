#!/bin/bash
# Script para corrigir permissões dos volumes
# Este script deve ser executado como root antes de iniciar o container

# Ajusta permissões dos volumes Docker
# Encontra o volume e ajusta permissões para UID 1000 (stockbit)

VOLUME_PATH=$(docker volume inspect stockbit_static_volume --format '{{ .Mountpoint }}' 2>/dev/null)
if [ -n "$VOLUME_PATH" ]; then
    echo "Ajustando permissões de static_volume..."
    sudo chown -R 1000:1000 "$VOLUME_PATH" 2>/dev/null || true
fi

VOLUME_PATH=$(docker volume inspect stockbit_media_volume --format '{{ .Mountpoint }}' 2>/dev/null)
if [ -n "$VOLUME_PATH" ]; then
    echo "Ajustando permissões de media_volume..."
    sudo chown -R 1000:1000 "$VOLUME_PATH" 2>/dev/null || true
fi

echo "Permissões ajustadas!"

