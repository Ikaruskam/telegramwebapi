import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import UserData
import requests
from dotenv import load_dotenv

# Загрузка переменных окружения из .env
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# Создаем таблицы в базе данных
UserData.metadata.create_all(bind=engine)

app = FastAPI()

# Создание сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Установка webhook при старте
@app.on_event("startup")
def setup_webhook():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook"
    response = requests.post(url, json={"url": WEBHOOK_URL})
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Webhook setup failed")

@app.post("/users/")
def create_user(user_id: str, name: str, weight: int, height: int, db: Session = Depends(get_db)):
    # Проверяем, не существует ли уже данные для этого пользователя
    user_data = db.query(UserData).filter(UserData.user_id == user_id).first()
    if user_data:
        raise HTTPException(status_code=400, detail="User data already exists")
    
    new_user = UserData(user_id=user_id, name=name, weight=weight, height=height)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/")
def read_user_data(user_id: str, db: Session = Depends(get_db)):
    user_data = db.query(UserData).filter(UserData.user_id == user_id).all()
    if not user_data:
        raise HTTPException(status_code=404, detail="User data not found")
    return user_data
