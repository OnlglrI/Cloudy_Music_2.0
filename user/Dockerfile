FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}

RUN npm install

COPY . .

# Сборка TypeScript
RUN npm run build

EXPOSE 8080

# Запуск сервера
CMD ["npm", "start"]
