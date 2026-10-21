
from fastapi import FastAPI, HTTPException

from product_repository import get_products
from fastapi import HTTPException, status
from psycopg import IntegrityError

from product_repository import create_product

from schemas import ProductCreate, ProductUpdate
from product_repository import update_product
from product_repository import delete_product

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


