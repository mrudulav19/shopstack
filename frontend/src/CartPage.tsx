
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./App.css";
import {
  getCart,
  getProducts,
  removeCartItem,
  type CartItem,
  type Product,
} from "./api";

function CartPage() {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [removingId, setRemovingId] = useState<number | null>(null);

  async function loadCart() {
    setLoading(true);
    setError("");

    try {
      const [cartItems, productList] = await Promise.all([
        getCart(),
        getProducts(),
      ]);

      setCart(cartItems);
      setProducts(productList);
    } catch {
      setError("Couldn't load your cart. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadCart();
  }, []);

  async function handleRemove(productId: number) {
    setRemovingId(productId);
    setError("");

    try {
      const updatedCart = await removeCartItem(productId);
      setCart(updatedCart);
    } catch {
      setError("Couldn't remove this item. Please try again.");
    } finally {
      setRemovingId(null);
    }
  }

  const cartCount = cart.reduce(
    (total, item) => total + item.quantity,
    0
  );

  const subtotal = cart.reduce((total, item) => {
    const product = products.find((p) => p.id === item.product_id);
    return total + (product?.price ?? 0) * item.quantity;
  }, 0);

  return (
    <main className="store">
      <header className="navbar">
        <Link className="brand" to="/">
          shopstack<span>.</span>
        </Link>

        <nav>
          <Link to="/">Continue shopping</Link>
        </nav>
      </header>

      <section className="catalog">
        <h1>Your cart</h1>
        <p>
          {cartCount} {cartCount === 1 ? "item" : "items"} in your cart
        </p>

        {loading && <p>Loading your cart...</p>}

        {error && (
          <p role="alert">
            {error}{" "}
            <button onClick={() => void loadCart()}>
              Try again
            </button>
          </p>
        )}

        {!loading && !error && cart.length === 0 && (
          <div className="empty-cart">
            <h2>Your cart is looking a little empty.</h2>
            <p>Find something you like and add it here.</p>
            <Link className="add-button" to="/">
              Browse products
            </Link>
          </div>
        )}

        {!loading && cart.length > 0 && (
          <>
            <div className="cart-items">
              {cart.map((item) => {
                const product = products.find(
                  (p) => p.id === item.product_id
                );

                return (
                  <article
                    className="cart-item"
                    key={item.product_id}
                  >
                    <div className="product-art">
                      <span>
                        {product?.name.slice(0, 1).toUpperCase() ?? "?"}
                      </span>
                    </div>

                    <div className="cart-item-info">
                      <h3>
                        {product?.name ?? `Product #${item.product_id}`}
                      </h3>
                      <p>Quantity: {item.quantity}</p>
                      <p>
                        ₹{(
                          (product?.price ?? 0) * item.quantity
                        ).toFixed(2)}
                      </p>
                    </div>

                    <button
                      className="remove-button"
                      onClick={() => void handleRemove(item.product_id)}
                      disabled={removingId === item.product_id}
                    >
                      {removingId === item.product_id
                        ? "Removing..."
                        : "Remove"}
                    </button>
                  </article>
                );
              })}
            </div>

            <div className="cart-summary">
              <h2>Subtotal: ₹{subtotal.toFixed(2)}</h2>
              <p>Shipping and taxes can be added at checkout.</p>
              <Link className="add-button" to="/">
                Continue shopping
              </Link>
            </div>
          </>
        )}
      </section>
    </main>
  );
}

export default CartPage;
