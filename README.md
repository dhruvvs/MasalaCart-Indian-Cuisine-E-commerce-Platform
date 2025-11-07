# MasalaCart — Indian Cuisine E‑commerce Platform

A full‑stack web application to browse Indian dishes, add items to a cart, and place orders. Built with Python/Django on the backend and HTML/CSS/JavaScript on the frontend.

> **Repository layout**: the project lives under `WSD_Project_final/ecommerce_site/` (this README is written for that directory structure).

## ✨ Features

* **Product catalog**: list pages with search/filter; dish detail pages with descriptions and pricing.
* **Cart & checkout**: add/update/remove items, order summary, and checkout flow.
* **User accounts**: sign up, login/logout, profile, and order history.
* **Admin & CRUD**: create/edit dishes, manage categories, prices, and inventory via Django admin.
* **Responsive UI**: mobile‑friendly pages with clean navigation.
* **Extensible payments**: code structured to plug in a payment provider (sandbox or live) later.

> If any of these are not implemented yet in your branch, treat them as the roadmap and check the TODOs section below.

## 🧱 Tech stack

* **Backend**: Python 3.x, Django 4.x (or 3.x)
* **Frontend**: HTML templates, CSS, vanilla JavaScript
* **Database**: SQLite (dev) — swap to Postgres/MySQL for production
* **Auth**: Django auth (sessions)
* **Tooling**: pip/venv, Django admin, collectstatic

## 📦 Project structure (high‑level)

```
WSD_Project_final/
└─ ecommerce_site/
   ├─ manage.py
   ├─ requirements.txt           # if present; otherwise see below
   ├─ ecommerce_site/            # project settings (settings.py, urls.py, wsgi.py)
   ├─ apps/                      # app modules if you grouped them (optional)
   │  ├─ products/               # catalog models, views, urls, templates
   │  ├─ cart/                   # cart session, views, urls, templates
   │  ├─ orders/                 # checkout, orders, models
   │  └─ users/                  # auth/profile, forms
   ├─ templates/                 # base.html, pages, includes
   ├─ static/                    # css/, js/, images/
   └─ docs/                      # screenshots, diagrams (optional)
```

> Your exact folders may differ; the README assumes standard Django conventions.

## 🚀 Quick start (local dev)

### 1) Clone & move into the project

```bash
git clone https://github.com/dhruvvs/MasalaCart-Indian-Cuisine-E-commerce-Platform.git
cd MasalaCart-Indian-Cuisine-E-commerce-Platform/WSD_Project_final/ecommerce_site
```

### 2) Create & activate a virtual environment

```bash
python -m venv .venv
# Windows
. .venv/Scripts/activate
# macOS/Linux
# source .venv/bin/activate
```

### 3) Install dependencies

If you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

If not, the minimum useful set is:

```bash
pip install "Django>=4.2,<5.0" pillow
```

### 4) Configure environment

Create a `.env` (or export vars) as needed:

```
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=change-me
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3   # optional if using default SQLite
```

### 5) Run migrations & create a superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 6) Load seed data (optional)

If you have a fixture file:

```bash
python manage.py loaddata seeds.json
```

### 7) Start the dev server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) and [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## 🛒 Usage walkthrough

1. Browse the catalog, open a dish page, and add items to the cart.
2. View the cart (header link), update quantities, proceed to checkout.
3. Sign in or register during checkout, confirm order.
4. Visit **My Orders** to see order history.

## 🔧 Configuration

* **Static files**: during development, Django serves static files automatically. For production, run `python manage.py collectstatic` and serve via the web server or a CDN.
* **Images**: ensure `MEDIA_ROOT`/`MEDIA_URL` are configured if you upload dish photos.
* **Payments**: the code is structured to allow Stripe/PayPal integration. Add provider keys as env vars and wire up the payment step.

## 🧪 Testing

```bash
python manage.py test
```

Add unit tests under each app (e.g., `products/tests/`, `orders/tests/`).

## 🔐 Security checklist (prod)

* Set `DEBUG = False` and `ALLOWED_HOSTS` correctly.
* Use a strong `SECRET_KEY` from env.
* Serve static/media via Nginx or S3‑style storage.
* Put Django behind Gunicorn/Uvicorn with a reverse proxy (Nginx/Caddy).
* Enforce HTTPS and secure cookies.
* Add a real database (PostgreSQL/MySQL) and rotate credentials.

## 📸 Screenshots

Place screenshots in `docs/` or `static/images/` and reference them here, e.g.:

```
![Home](docs/home.png)
![Cart](docs/cart.png)
![Checkout](docs/checkout.png)
```

## 🗺️ Roadmap / TODOs

* [ ] Add product filters (cuisine, spice level, veg/non‑veg)
* [ ] Search autosuggest
* [ ] Discount codes / offers
* [ ] Payment gateway integration
* [ ] Email notifications for orders
* [ ] Comprehensive tests & CI (GitHub Actions)

## 🧰 Helpful commands

```bash
# make database migrations when you change models
python manage.py makemigrations && python manage.py migrate

# create a new Django app
python manage.py startapp <appname>

# collect static files (prod)
python manage.py collectstatic
```

## 🗃️ Example `requirements.txt`

```
Django>=4.2,<5.0
pillow
python-dotenv
psycopg[binary]>=3.2  # if using PostgreSQL
```

## 📄 License

Add a license of your choice (e.g., MIT) under `LICENSE`.

## 🙌 Acknowledgements

* Built as part of a web systems/dev project.
* Thanks to open‑source Django community for templates and examples.

---

**Maintainer**: Dhruv Patel (GitHub: @dhruvvs)

If you spot mismatches between this README and the code, open an issue or PR and we’ll update it.
