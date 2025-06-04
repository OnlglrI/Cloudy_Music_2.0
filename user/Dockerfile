FROM node:18-alpine

# Рабочая директория
WORKDIR /app

# Копируем package.json и package-lock.json
COPY package*.json ./

# Указываем аргумент сборки
ARG NODE_ENV=production

# Пробрасываем аргумент как переменную окружения
ENV NODE_ENV=${NODE_ENV}

# Устанавливаем зависимости
RUN npm install

# Установка nodemon только в режиме разработки
RUN if [ "$NODE_ENV" = "development" ]; then npm install -g nodemon; fi

# Копируем остальной код
COPY . .

# Открываем порт
EXPOSE 3000

# Команда запуска в зависимости от NODE_ENV
CMD [ "sh", "-c", "if [ \"$NODE_ENV\" = \"development\" ]; then nodemon index.js; else node index.js; fi" ]
