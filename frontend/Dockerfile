# syntax=docker/dockerfile:1

FROM node:20-alpine

WORKDIR /app

# Copia únicamente los manifiestos primero para aprovechar la cache de capas
COPY package.json package-lock.json* ./

RUN npm install

# Copia el resto del código fuente
COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev"]
