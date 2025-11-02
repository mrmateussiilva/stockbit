#!/bin/bash

set -e

echo "Aguardando PostgreSQL estar pronto..."

# Aguarda o banco de dados estar disponível (máximo 60 tentativas = 2 minutos)
MAX_RETRIES=60
RETRY_COUNT=0

until pg_isready -h "${POSTGRES_HOST:-db}" -p "${POSTGRES_PORT:-5432}" -U "${POSTGRES_USER:-stockbit}" || [ $RETRY_COUNT -eq $MAX_RETRIES ]; do
  RETRY_COUNT=$((RETRY_COUNT + 1))
  echo "PostgreSQL não está disponível ainda - aguardando... (tentativa $RETRY_COUNT/$MAX_RETRIES)"
  sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
  echo "ERRO: PostgreSQL não ficou disponível após $MAX_RETRIES tentativas!"
  exit 1
fi

echo "PostgreSQL está pronto!"

# Muda para o usuário não-root
export USER=stockbit
export HOME=/home/stockbit

# Executa migrações
echo "Executando migrações..."
python manage.py migrate --noinput

# Coleta arquivos estáticos
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput || echo "Aviso: Erro ao coletar arquivos estáticos (pode ser normal se já foram coletados)"

# Cria superusuário se não existir (opcional - descomente se necessário)
# echo "Criando superusuário..."
# python manage.py shell << EOF
# from django.contrib.auth import get_user_model
# User = get_user_model()
# if not User.objects.filter(username='admin').exists():
#     User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
#     print('Superusuário criado: admin / admin123')
# EOF

# Inicia a aplicação
echo "Iniciando aplicação..."
exec "$@"

