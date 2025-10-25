FROM node:18-alpine

# Define o diretório de trabalho
WORKDIR /app

# Copia package.json e package-lock.json
COPY package*.json ./

# Instala dependências
RUN npm install

# Copia o código da aplicação
COPY . .

# Expõe a porta
EXPOSE 5173

# Comando para executar a aplicação
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]


