# Используем базовый образ Python
FROM python:3.11.9-slim

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Копируем исходный код
COPY . .

# Указываем переменные окружения
ENV DATABASE_URL="sqlite:///./test.db"
ENV TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
ENV WEBHOOK_URL=$WEBHOOK_URL

CMD [ "python", "main.py" ]
