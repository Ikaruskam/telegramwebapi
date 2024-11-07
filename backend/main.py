import random
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel  # Импортируем BaseModel из pydantic для работы с моделями
import uvicorn

app = FastAPI()

# CORS для фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tvoitrenerbot.ru"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Модель данных для входящих сообщений
class Message(BaseModel):
    user_id: int
    username: str
    text: str

# Простой роут для получения данных пользователя из Telegram
@app.post("/api/user_data")
async def get_user_data(request: Request, message: Message):
    # Здесь вы можете обработать данные и сохранить их в БД
    return {"status": "success", "message": "User data received"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
