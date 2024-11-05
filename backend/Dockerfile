# backend/Dockerfile
FROM python:3.11.9-slim

# Установка зависимостей
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Создание директории для хранения базы данных
RUN mkdir /data

# Копирование приложения
COPY . .

# Установка переменной окружения для SQLite
ENV DATABASE_URL="sqlite:////data/items.db"

CMD [ "python", "main.py" ]
