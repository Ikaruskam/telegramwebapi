import random
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Список элементов
items = [
    {
        "id": 1,
        "name": "Docker",
        "weight": 10,
        "height": 20,
        "img": "https://static-00.iconduck.com/assets.00/docker-icon-2048x2048-5mc7mvtn.png",
    },
    {
        "id": 2,
        "name": "Nginx",
        "weight": 15,
        "height": 25,
        "img": "https://www.svgrepo.com/show/373924/nginx.svg",
    },
    {
        "id": 3,
        "name": "GitHub",
        "weight": 20,
        "height": 30,
        "img": "https://cdn-icons-png.flaticon.com/512/25/25231.png",
    },
]

# Модель для нового элемента с дополнительными полями weight и height
class Item(BaseModel):
    name: str
    weight: float
    height: float
    img: str = "https://example.com/default-image.png"  # Задаем изображение по умолчанию

@app.get("/items")
def get_items():
    random.shuffle(items)
    return items

@app.post("/add_item")
def add_item(item: Item):
    # Добавляем новый элемент с уникальным id
    new_item = {
        "id": len(items) + 1,
        "name": item.name,
        "weight": item.weight,
        "height": item.height,
        "img": item.img,
    }
    items.append(new_item)
    return {"message": "Item added successfully", "items": items}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tvoitrenerbot.ru"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
