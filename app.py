from pydantic import BaseModel, Field
from fastapi import HTTPException
from product_repository import reduce_stock
from fastapi import FastAPI, HTTPException, status
from psycopg import IntegrityError
from fastapi.middleware.cors import CORSMiddleware
from product_repository import (
    get_products,
    create_product,
    update_product,
    delete_product,
)
from schemas import ProductCreate, ProductUpdate

app = FastAPI(
    title="ShopStack API",
    description="E-commerce backend learning project",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Welcome to ShopStack API"}


@app.get("/products")
def list_products():
    try:
        return get_products()
    except Exception as e:
        print(f"ERROR in list_products: {e!r}", flush=True)
        raise HTTPException(
            status_code=500,
            detail="Could not retrieve products",
        )
        

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product_endpoint(product: ProductCreate):
    try:
        return create_product(
            product.id,
            product.name,
            product.price,
            product.stock,
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A product with this ID already exists",
        )


@app.put("/products/{product_id}")
def update_product_endpoint(
    product_id: int,
    product: ProductUpdate,
):
    try:
        updated_product = update_product(
            product_id,
            product.price,
            product.stock,
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not update product",
        )

    if updated_product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return updated_product


@app.delete("/products/{product_id}")
def delete_product_endpoint(product_id: int):
    try:
        deleted = delete_product(product_id)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Could not delete product",
        )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return {
        "message": f"Product {product_id} deleted successfully"
    }


class StockReduction(BaseModel):
    quantity: int = Field(default=1, gt=0)


@app.post("/products/{product_id}/reduce-stock")
def reduce_product_stock(product_id: int, request: StockReduction):
    product = reduce_stock(product_id, request.quantity)

    if product is None:
        raise HTTPException(
            status_code=409,
            detail="Product not found or insufficient stock",
        )

    return product



