
from fastapi import FastAPI, HTTPException

from product_repository import get_products

app = FastAPI(
    title="ShopStack API",
    description="E-commerce backend learning project",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Welcome to ShopStack API"}


@app.get("/products")
def list_products():
    try:
        return get_products()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve products",
        )
