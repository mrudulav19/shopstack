
from product_repository import get_products


def test_get_products_returns_database_records():
    products = get_products()

    assert len(products) >= 3

    keyboard = next(
        product
        for product in products
        if product["id"] == 1
    )

    assert keyboard["name"] == "Keyboard"
    assert keyboard["stock"] == 10
