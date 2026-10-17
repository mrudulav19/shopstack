
from db import get_connection


def get_products():
    query = """
        SELECT id, name, price, stock
        FROM products
        ORDER BY id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

    products = []

    for row in rows:
        product = {
            "id": row[0],
            "name": row[1],
            "price": float(row[2]),
            "stock": row[3],
        }
        products.append(product)

    return products

def create_product(product_id, name, price, stock):
    query = """
        INSERT INTO products (id, name, price, stock)
        VALUES (%s, %s, %s, %s)
        RETURNING id, name, price, stock
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (product_id, name, price, stock),
            )
            row = cursor.fetchone()

    return {
        "id": row[0],
        "name": row[1],
        "price": float(row[2]),
        "stock": row[3],
    }


def update_product(product_id, price, stock):
    query = """
        UPDATE products
        SET price = %s, stock = %s
        WHERE id = %s
        RETURNING id, name, price, stock
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                query,
                (price, stock, product_id),
            )
            row = cursor.fetchone()

    if row is None:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "price": float(row[2]),
        "stock": row[3],
    }


def delete_product(product_id):
    query = """
        DELETE FROM products
        WHERE id = %s
        RETURNING id
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(query, (product_id,))
            row = cursor.fetchone()

    return row is not None



if __name__ == "__main__":
    for product in get_products():
        print(product)
