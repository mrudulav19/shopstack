
export type Product = {
  id: number;
  name: string;
  price: number;
  stock: number;
  image_url: string | null;
};

export type CartItem = {
  product_id: number;
  quantity: number;
};

export const PRODUCT_API = "http://localhost:8000";
export const CART_API = "http://localhost:8001";
export const USER_ID = 1;

export async function getProducts(): Promise<Product[]> {
  const response = await fetch(`${PRODUCT_API}/products`);

  if (!response.ok) {
    throw new Error("Unable to load products");
  }

  return response.json();
}

export async function getCart(): Promise<CartItem[]> {
  const response = await fetch(`${CART_API}/cart/${USER_ID}`);

  if (!response.ok) {
    throw new Error("Unable to load cart");
  }

  const data = await response.json();
  return data.items ?? [];
}

export async function addCartItem(
  productId: number,
  quantity = 1
): Promise<CartItem[]> {
  const response = await fetch(
    `${CART_API}/cart/${USER_ID}/items`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        product_id: productId,
        quantity,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Unable to add item to cart");
  }

  const data = await response.json();
  return data.items ?? [];
}

export async function removeCartItem(
  productId: number
): Promise<CartItem[]> {
  const response = await fetch(
    `${CART_API}/cart/${USER_ID}/items/${productId}`,
    { method: "DELETE" }
  );

  if (!response.ok) {
    throw new Error("Unable to remove item from cart");
  }

  const data = await response.json();
  return data.items ?? [];
}
