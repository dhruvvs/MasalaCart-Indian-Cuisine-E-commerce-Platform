# MasalaCart – Indian Cuisine E-commerce Platform 🍛🛒

MasalaCart is a full-stack e-commerce web application themed around an Indian restaurant.  
It’s built with **Django** on the backend and **HTML/CSS/Bootstrap + JavaScript** on the frontend, and is designed to feel like a small, production-style online food ordering system.

---

## 🌟 Key Features

### 🧑‍🍳 Customer Experience

- **User Authentication**
  - Signup, login, logout using Django’s auth system.
  - Authenticated users can place orders and see their order history.

- **Product Browsing**
  - Dishes (products) stored in the database with name, category, price, and image.
  - Backend-powered **search**, **category filters**, and **pagination**.
  - **Most Popular Dishes** section, based on how often each dish is added to cart.

- **Cart & Checkout Flow**
  - Session-based **shopping cart**:
    - Add to cart from the product listing page.
    - Update quantities (+/–) directly from the cart page.
    - Remove items when quantity drops to zero.
  - **Checkout**:
    - Captures shipping details (name, phone, address, city, state, zip).
    - Saves shipping info in an `Address` profile linked to the user.
    - Reuses saved address details for faster repeat orders.

- **Orders & Re-order**
  - Each checkout creates:
    - An `Order` with `total_quantity`, `total_price`, and `status`.
    - `OrderItem`s that store the **price at purchase time** (not just current product price).
  - **My Orders** page:
    - Lists full order history for the logged-in user.
    - Shows shipping details and line items.
    - Includes a **“Re-order this”** button that rebuilds the cart from any past order.

---

## 🧠 Why This Project

This project is meant to show more than a basic CRUD app. It demonstrates:

- A **complete e-commerce flow**:
  > Auth → product browsing → search/filter → cart → checkout → order history → re-order.
- A **responsive UI** that works nicely on both mobile and desktop.
- Realistic **UX flows** like re-ordering, popular items, and address reuse.
- A codebase that’s **extensible** for:
  - Real payment integration (Stripe, etc.)
  - Inventory management
  - Admin dashboards
  - Frontend frameworks (React, mobile clients) via APIs.

---

## 🛠️ Tech Stack

**Backend**

- Python 3.x
- Django
- Django REST Framework (DRF) – for API endpoints
- SQLite (for development; can be swapped for Postgres/MySQL)

**Frontend**

- Django templates
- HTML5, CSS3
- Bootstrap 5
- Vanilla JavaScript (for interactive cart behavior and UX tweaks)

---

## 🧱 Core Architecture

### Models (in `ecommerce_app/models.py`)

- `Product`
  - `name`, `category`, `price`, `image_name`
  - `times_added_to_cart` (analytics: how often this dish was added to cart)

- `Order`
  - Linked to `User`
  - `total_quantity`, `total_price`
  - `status` (`PENDING`, `PAID`, `CANCELLED`)
  - Shipping info: `full_name`, `phone`, `street`, `city`, `state`, `zip_code`

- `OrderItem`
  - `order` → `Order`
  - `product` → `Product`
  - `quantity`
  - `price_at_purchase` (captures price at the moment of checkout)
  - `line_total()` helper

- `Address`
  - Linked to `User`
  - Used to prefill shipping details at checkout for repeat orders.

### Views & Flows (in `ecommerce_app/views.py`)

- `product`
  - Lists products with:
    - Optional `?q=` search
    - Optional `?category=` filter
    - Pagination
  - Shows “Most Popular Dishes” based on `times_added_to_cart`.

- `add_to_cart`, `update_cart`
  - Store cart items in `request.session["cart"]`.
  - `times_added_to_cart` is updated whenever items are added or incremented.

- `cartDetails`
  - Builds a cart context from the session.
  - Shows cart items, totals, and a combined Checkout + Shipping form.
  - Prefills shipping fields from the user’s saved `Address`, if it exists.

- `place_order`
  - Validates cart & shipping data.
  - Saves/updates `Address` for the user.
  - Creates `Order` + `OrderItem`s.
  - Clears the cart and redirects to a Thank You page.

- `my_orders`
  - Lists all past orders for the user with items and shipping info.

- `reorder_order`
  - Takes a past `Order`, rebuilds the current session cart with its items, and redirects the user back to the cart.

### API Endpoints (DRF)

- `GET /api/products/`
  - Optional `?q=` and `?category=` parameters for search and filtering.
- `GET /api/cart/`
  - Returns the current session cart (items, totals) as JSON.

These endpoints make it easy to plug in a React/Next.js frontend or mobile app later.

---

## 🚀 Getting Started (Local Development)

### 1. Clone the Repository

```bash
git clone https://github.com/dhruvvs/MasalaCart-Indian-Cuisine-E-commerce-Platform.git
cd MasalaCart-Indian-Cuisine-E-commerce-Platform/WSD_Project_final/ecommerce_site

