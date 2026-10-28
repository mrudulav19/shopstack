
import { useEffect, useState } from "react";
import { Link, Route, Routes, useNavigate } from "react-router-dom";
import "./App.css";
import CartPage from "./Cartpage";
import { getCart, getProducts, addCartItem, type CartItem, type Product } from "./api";

function Storefront() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [cart, setCart] = useState<CartItem[]>([]);
  const [addingId, setAddingId] = useState<number | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    getProducts()
      .then(setProducts)
      .catch(() => setError("Couldn't load products. Please try again."))
      .finally(() => setLoading(false));

    getCart()
      .then(setCart)
      .catch((err) => console.error("Could not load cart:", err));
  }, []);

  async function addToCart(productId: number) {
    setAddingId(productId);
    setError("");

    try {
      const updatedCart = await addCartItem(productId);
setCart(updatedCart);

const refreshedProducts = await getProducts();
setProducts(refreshedProducts);
    } catch (err) {
      console.error("Could not add item:", err);
      setError("Couldn't add this item. Please check the Cart Service.");
    } finally {
      setAddingId(null);
    }
  }

  const cartCount = cart.reduce(
    (total, item) => total + item.quantity,
    0
  );

  return (
    <main className="store">
      <header className="navbar">
        <Link className="brand" to="/">
          shopstack<span>.</span>
        </Link>

        <nav>
          <a href="#products">Products</a>
          <a href="#about">About</a>
          <button className="cart-button" onClick={() => navigate("/cart")}>
            Cart ({cartCount})
          </button>
        </nav>
      </header>

      <section className="hero">
        <p className="eyebrow">THE SHOPSTACK COLLECTION</p>
        <h1>Good things.<br />Simply chosen.</h1>
        <p>Everyday essentials, picked with care.</p>
        <a className="add-button" href="#products">Explore products</a>
      </section>

      <section className="catalog" id="products">
        <h2>Our products</h2>

        {loading && <p>Loading products...</p>}
        {error && <p role="alert">{error}</p>}

        {!loading && !error && products.length === 0 && (
          <p>No products available yet.</p>
        )}

        <div className="product-grid">
          {products.map((product) => (
            <article className="product-card" key={product.id}>
            
<div className="product-art">
  {product.image_url ? (
    <img
      src={product.image_url}
      alt={product.name}
      loading="lazy"
    />
  ) : (
    <span>{product.name.slice(0, 1).toUpperCase()}</span>
  )}
</div>


              <div className="product-info">
                <h3>{product.name}</h3>
                <p>{product.stock > 0 ? `${product.stock} in stock` : "Out of stock"}</p>
                <strong>₹{Number(product.price).toFixed(2)}</strong>
              </div>

              <button
                className="add-button"
                onClick={() => void addToCart(product.id)}
                disabled={product.stock <= 0 || addingId === product.id}
              >
                {addingId === product.id
                  ? "Adding..."
                  : product.stock > 0
                    ? "Add to cart +"
                    : "Out of stock"}
              </button>
            </article>
          ))}
        </div>
      </section>

      <footer id="about">
        <Link className="brand" to="/">shopstack<span>.</span></Link>
        <p>Everyday essentials, simply chosen.</p>
      </footer>
    </main>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Storefront />} />
      <Route path="/cart" element={<CartPage />} />
    </Routes>
  );
}

export default App;
