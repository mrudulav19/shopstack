
import os

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from db import get_connection

PRODUCT_API = os.getenv("PRODUCT_API", "http://localhost:8000")

app = FastAPI(
    title="ShopStack Cart Service",
    description="Shopping cart microservice",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, gt=0)


def read_cart(user_id: int):
    query = """
        SELECT product_id, quantity
        FROM cart_items
        WHERE user_id = %s
        ORDER BY id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (user_id,))
            rows = cursor.fetchall()

    return [
        {"product_id": row[0], "quantity": row[1]}
        for row in rows
    ]


@app.get("/")
def home():
    return {"message": "Welcome to ShopStack Cart Service"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/cart/{user_id}")
def get_cart(user_id: int):
    items = read_cart(user_id)

    return {
        "user_id": user_id,
        "items": items,
        "item_count": sum(item["quantity"] for item in items),
    }


@app.post("/cart/{user_id}/items")
def add_item(user_id: int, item: CartItemCreate):
    # Reduce product stock before updating the cart.
    try:
        response = httpx.post(
            f"{PRODUCT_API}/products/{item.product_id}/reduce-stock",
            json={"quantity": item.quantity},
            timeout=5.0,
        )
    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Product Service is unavailable",
        )

    if response.status_code == 409:
        raise HTTPException(
            status_code=409,
            detail="Product not found or insufficient stock",
        )

    if not response.is_success:
        raise HTTPException(
            status_code=502,
            detail="Could not update product stock",
        )

    query = """
        INSERT INTO cart_items (user_id, product_id, quantity)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, product_id)
        DO UPDATE SET quantity = cart_items.quantity + EXCLUDED.quantity
    """

    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    query,
                    (user_id, item.product_id, item.quantity),
                )
    except Exception:
        # Compensate for the stock reduction if the cart save fails.
        try:
            httpx.post(
                f"{PRODUCT_API}/products/{item.product_id}/increase-stock",
                json={"quantity": item.quantity},
                timeout=5.0,
            )
        except httpx.RequestError:
            pass

        raise HTTPException(
            status_code=500,
            detail="Could not save cart item",
        )

    return {
        "message": "Item added to cart",
        "items": read_cart(user_id),
        "product": response.json(),
    }


@app.delete("/cart/{user_id}/items/{product_id}")
def remove_item(user_id: int, product_id: int):
    query = """
        DELETE FROM cart_items
        WHERE user_id = %s AND product_id = %s
        RETURNING product_id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (user_id, product_id))
            deleted = cursor.fetchone()

    if deleted is None:
        raise HTTPException(
            status_code=404,
            detail="Cart item not found",
        )

    return {
        "message": "Item removed from cart",
        "items": read_cart(user_id),
    }
