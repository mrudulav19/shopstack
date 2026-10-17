
import os

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "shopstack_db"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASSWORD"),
        connect_timeout=5,
    )


if __name__ == "__main__":
    try:
        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT current_database(), version()"
                )
                result = cursor.fetchone()

                print("Connected successfully!")
                print(f"Database: {result[0]}")
                print(f"PostgreSQL version: {result[1]}")

    except psycopg.OperationalError as error:
        print("Could not connect to PostgreSQL.")
        print(f"Error: {error}")
