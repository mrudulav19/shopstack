
from main import add_to_cart, display_cart


def sample_products():
    return [
        {
            "id": 1,
            "name": "Keyboard",
            "price": 1499.99,
            "stock": 10,
        },
        {
            "id": 2,
            "name": "Mouse",
            "price": 599.00,
            "stock": 20,
        },
    ]


def test_add_product_to_cart(monkeypatch):
    products = sample_products()
    cart = []

    answers = iter(["1", "2"])
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(answers),
    )

    add_to_cart(products, cart)

    assert cart == [
        {"product_id": 1, "quantity": 2}
    ]


def test_reject_quantity_above_stock(monkeypatch):
    products = sample_products()
    cart = []

    answers = iter(["1", "11"])
    monkeypatch.setattr(
        "builtins.input",
        lambda prompt: next(answers),
    )

    add_to_cart(products, cart)

    assert cart == []


def test_display_cart_total(capsys):
    products = sample_products()
    cart = [
        {"product_id": 1, "quantity": 2}
    ]

    display_cart(products, cart)

    output = capsys.readouterr().out

    assert "Keyboard" in output
    assert "2999.98" in output
