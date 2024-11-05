import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./items.db"  # Путь к вашей базе данных SQLite

# Настройка SQLAlchemy
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Модель для элемента
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    weight = Column(Float)
    height = Column(Float)

# Создание таблицы
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Модель для входящих данных
class ItemCreate(BaseModel):
    name: str
    weight: float
    height: float

@app.post("/add_item")
def add_item(item: ItemCreate):
    db = SessionLocal()
    db_item = Item(name=item.name, weight=item.weight, height=item.height)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    db.close()
    return {"message": "Item added successfully", "item": db_item}

@app.get("/items")
def get_items():
    db = SessionLocal()
    items = db.query(Item).all()
    db.close()
    return items

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tvoitrenerbot.ru"],  # Добавьте другие разрешенные источники при необходимости
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
