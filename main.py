
import json


def load_products():
    with open("data/products.json", "r") as file:
        products = json.load(file)

    return products


def display_products(products):
    print("\n========== SHOPSTACK ==========")
    print("Available Products\n")

    for product in products:
        print(
            f'ID: {product["id"]} | '
            f'{product["name"]} | '
            f'₹{product["price"]:.2f} | '
            f'Stock: {product["stock"]}'
        )


def add_to_cart(products, cart):
    product_id = int(input("Enter product ID: "))
    quantity = int(input("Enter quantity: "))

    # Find the requested product
    selected_product = None

    for product in products:
        if product["id"] == product_id:
            selected_product = product
            break

    # Check whether the product exists
    if selected_product is None:
        print("Product not found!")
        return

    # Check whether the quantity is valid
    if quantity <= 0:
        print("Quantity must be greater than zero!")
        return

    # Find this product in the existing cart
    cart_item = None

    for item in cart:
        if item["product_id"] == product_id:
            cart_item = item
            break

    # Account for items already in the cart
    current_quantity = 0

    if cart_item is not None:
        current_quantity = cart_item["quantity"]

    if current_quantity + quantity > selected_product["stock"]:
        print("Not enough stock available!")
        return

    # Add a new item or update an existing one
    if cart_item is not None:
        cart_item["quantity"] += quantity
    else:
        cart.append({
            "product_id": product_id,
            "quantity": quantity
        })

    print(f'{selected_product["name"]} added to cart!')


def display_cart(products, cart):
    print("\n========== YOUR CART ==========")

    if not cart:
        print("Your cart is empty.")
        return

    grand_total = 0

    for item in cart:
        for product in products:
            if product["id"] == item["product_id"]:
                subtotal = product["price"] * item["quantity"]
                grand_total += subtotal

                print(
                    f'{product["name"]} x {item["quantity"]} '
                    f'= ₹{subtotal:.2f}'
                )

    print(f"\nGrand total: ₹{grand_total:.2f}")



def main():
    products = load_products()
    cart = []

    while True:
        print("\n========== SHOPSTACK ==========")
        print("1. View products")
        print("2. Add to cart")
        print("3. View cart")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            display_products(products)

        elif choice == "2":
            try:
                add_to_cart(products, cart)
            except ValueError:
                print("Please enter valid numbers.")

        elif choice == "3":
            display_cart(products, cart)

        elif choice == "4":
            print("Thanks for shopping with ShopStack!")
            break

        else:
            print("Invalid option. Please choose 1–4.")


if __name__ == "__main__":
    main()

