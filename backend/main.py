import os
from fastapi import FastAPI, Request, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
import requests
from models import Base, User

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем токен и URL webhook из .env файла
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем соединение с базой данных
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Создаем все таблицы, если их еще нет
Base.metadata.create_all(bind=engine)

# Инициализация FastAPI
app = FastAPI()

@app.post("/webhook")
async def webhook(request: Request):
    """
    Обрабатывает запросы от Telegram через webhook.
    Извлекает данные пользователя (user_id, first_name, username)
    и сохраняет их в базе данных.
    """
    payload = await request.json()
    print("Полученные данные от Telegram:", payload)

    # Извлекаем информацию о пользователе
    if "message" in payload:
        message = payload["message"]
        user_id = message["from"]["id"]
        first_name = message["from"].get("first_name")
        last_name = message["from"].get("last_name")
        username = message["from"].get("username")

        # Создаем сессию для работы с базой данных
        db = SessionLocal()

        # Проверяем, существует ли уже такой пользователь в базе данных
        db_user = db.query(User).filter(User.user_id == user_id).first()

        if not db_user:
            # Если пользователя нет в базе, создаем нового
            new_user = User(user_id=user_id, first_name=first_name, last_name=last_name, username=username)
            db.add(new_user)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                return {"status": "error", "message": "Ошибка при сохранении пользователя"}
            print(f"Пользователь {first_name} {last_name} добавлен в базу данных.")

        db.close()

    return {"status": "success"}

# Устанавливаем webhook при запуске приложения
def set_webhook():
    """
    Устанавливает webhook для Telegram бота, чтобы получать данные от Telegram.
    """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    response = requests.post(url, json={'url': WEBHOOK_URL})
    
    if response.status_code == 200:
        print("Webhook успешно установлен.")
    else:
        print(f"Ошибка при установке webhook: {response.text}")

# Вызовем установку webhook при запуске приложения
set_webhook()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
