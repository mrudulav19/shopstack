
from product_repository import (
    create_product,
    get_products,
    update_product,
    delete_product,
)


def main():
    product_id = 999

    try:
        # CREATE
        product = create_product(
            product_id, "Test Product", 100.00, 5
        )
        print("Created:", product)

        # READ
        products = get_products()
        assert any(p["id"] == product_id for p in products)
        print("Read: product found")

        # UPDATE
        updated = update_product(product_id, 120.00, 8)
        assert updated is not None
        assert updated["price"] == 120.00
        assert updated["stock"] == 8
        print("Updated:", updated)

    finally:
        # DELETE, even if an earlier assertion fails
        deleted = delete_product(product_id)
        print("Deleted:", deleted)


if __name__ == "__main__":
    main()
