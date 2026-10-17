from db import get_connection


def get_products():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, price, stock
                FROM products
                ORDER BY id
                """
            )
            return cursor.fetchall()


if __name__ == "__main__":
    for product in get_products():
        print(product)