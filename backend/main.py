import os
import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import requests

# Загружаем переменные окружения
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = FastAPI()

# Настройка базы данных SQLite с SQLAlchemy
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Пример модели для хранения данных
class Item(Base):
    tablename = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Integer)
    height = Column(Integer)

Base.metadata.create_all(bind=engine)

@app.post("/items/")
def create_item(name: str, weight: int, height: int, db: SessionLocal = Depends()):
    item = Item(name=name, weight=weight, height=height)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

# Устанавливаем webhook для Telegram
def set_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    response = requests.post(url, json={'url': WEBHOOK_URL})
    if response.status_code == 200:
        print("Webhook установлен")
    else:
        print("Ошибка установки webhook:", response.text)

set_webhook()
