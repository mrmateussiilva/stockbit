#!/bin/bash

echo "=== Verificando portas em uso ==="
echo ""

echo "Porta 80:"
sudo lsof -i :80 || echo "Porta 80 está livre"
echo ""

echo "Porta 443:"
sudo lsof -i :443 || echo "Porta 443 está livre"
echo ""

echo "=== Serviços do Docker na porta 443 ==="
docker ps --filter "publish=443" --format "table {{.ID}}\t{{.Names}}\t{{.Ports}}"

echo ""
echo "=== Processos usando portas 80 e 443 ==="
sudo netstat -tlnp | grep -E ':(80|443) ' || echo "Nenhum processo encontrado"

