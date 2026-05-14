from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import auth, products, orders

app = FastAPI(title="FastAPI Ecommerce Backend")

app.mount(
    "/uploads",
    StaticFiles(directory="app/uploads"),
    name="uploads"
)

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)

@app.get("/")
async def home():
    return {"message": "FastAPI Ecommerce Backend"}
