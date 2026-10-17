
CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price NUMERIC(10, 2) NOT NULL CHECK (price >= 0),
    stock INTEGER NOT NULL CHECK (stock >= 0)
);


INSERT INTO products (id, name, price, stock)
VALUES
    (1, 'Keyboard', 1499.99, 10),
    (2, 'Mouse', 599.00, 20),
    (3, 'Headphones', 999.00, 15);
