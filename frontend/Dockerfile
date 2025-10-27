FROM node:18-alpine

# Instala pnpm globalmente
RUN npm install -g pnpm

# Define o diretório de trabalho
WORKDIR /app

# Copia package.json e pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Instala dependências usando pnpm
RUN pnpm install --frozen-lockfile

# Copia o código da aplicação
COPY . .

# Expõe a porta
EXPOSE 5173

# Comando para executar a aplicação
CMD ["pnpm", "run", "dev", "--", "--host", "0.0.0.0"]


