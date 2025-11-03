# Dockerfile para produção - StockBit
FROM python:3.12-slim

# Define variáveis de ambiente
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Cria diretório de trabalho
WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia o código da aplicação
COPY . .

# Copia e configura o entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Cria usuário não-root para segurança
RUN useradd -m -u 1000 stockbit && \
    chown -R stockbit:stockbit /app && \
    chmod +x /entrypoint.sh

# Cria diretórios que serão montados como volumes e garante permissões
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R stockbit:stockbit /app/staticfiles /app/media

# Muda para usuário não-root antes do entrypoint
USER stockbit

# Expõe a porta
EXPOSE 8000

# Entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Comando padrão
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "stockbit.wsgi:application"]

