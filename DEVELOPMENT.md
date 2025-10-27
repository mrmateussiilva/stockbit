# Configuração de desenvolvimento para Stockbit
# Este arquivo contém todas as configurações necessárias para desenvolvimento

# ===========================================
# CONFIGURAÇÕES DO DOCKER
# ===========================================

# Arquivos de configuração Docker Compose
DOCKER_COMPOSE_DEV=docker-compose.dev.yml
DOCKER_COMPOSE_PROD=docker-compose.prod.yml

# Portas dos serviços
FRONTEND_PORT=5173
BACKEND_PORT=8000

# ===========================================
# CONFIGURAÇÕES DO FRONTEND
# ===========================================

# URL da API
VITE_API_URL=http://localhost:8000/api

# Configurações de hot reload
CHOKIDAR_USEPOLLING=true
WATCHPACK_POLLING=true

# ===========================================
# CONFIGURAÇÕES DO BACKEND
# ===========================================

# Configurações do Django
SECRET_KEY=django-insecure-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0,backend

# ===========================================
# COMANDOS ÚTEIS
# ===========================================

# Para iniciar o desenvolvimento:
# ./dev.sh start

# Para ver os logs:
# ./dev.sh logs

# Para parar os serviços:
# ./dev.sh stop

# Para reconstruir as imagens:
# ./dev.sh build

# Para limpar tudo:
# ./dev.sh clean

# Para produção:
# ./dev.sh prod



