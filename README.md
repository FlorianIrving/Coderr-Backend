# Coderr Backend – Django REST API

Coderr is the backend for a freelancing platform that connects clients and developers.  
It provides secure registration, authentication, profile management, offer creation, order processing, and review features.

---

## 🔧 Tech Stack

- **Framework:** Django 5.2, Django REST Framework
- **Auth:** Token-based Authentication
- **Database:** SQLite (default), PostgreSQL-ready
- **Deployment Ready:** Yes (e.g. via Gunicorn & Docker)
- **API Access:** JSON (REST)

---

## 🚀 Features

### 🧑 User Authentication & Profiles

- Token-based registration & login
- Role-based profiles: `customer` or `business`
- Updateable profile with avatar, location, phone, etc.

### 💼 Offers & Details

- Businesses can create offers with multiple detail packages
- Each detail (e.g. basic, pro, premium) includes price, features & delivery time

### 📦 Orders

- Customers can order specific offer details
- Business users can update the order status

### 🌟 Reviews

- Authenticated users can review businesses
- Rating (1–5), text feedback, and average rating system

### 📊 Public Metrics

- Public base info endpoint (e.g. `review_count`, `offer_count`, `avg_rating`)

---

## 🔑 Authentication

All endpoints (except registration & login) require an auth token.

**Example request header:**

```
Authorization: Token your_token_here
```

---

## 📘 API Endpoints (English)

| Method | Endpoint                           | Description                          |
| ------ | ---------------------------------- | ------------------------------------ |
| POST   | `/api/registration/`               | Register a new user                  |
| POST   | `/api/login/`                      | Login and get token                  |
| GET    | `/api/profile/<id>/`               | Get user profile by ID               |
| PATCH  | `/api/profile/<id>/`               | Update own profile                   |
| GET    | `/api/profiles/business/`          | List all business profiles           |
| GET    | `/api/profiles/customer/`          | List all customer profiles           |
| GET    | `/api/offers/`                     | List all offers (with filters)       |
| POST   | `/api/offers/`                     | Create new offer with details        |
| GET    | `/api/offers/<id>/`                | Offer detail view                    |
| PATCH  | `/api/offers/<id>/`                | Update specific offer (and details)  |
| GET    | `/api/offerdetails/<id>/`          | Get single offer detail              |
| GET    | `/api/orders/`                     | List user-related orders             |
| POST   | `/api/orders/`                     | Place a new order                    |
| PATCH  | `/api/orders/<id>/`                | Update status (business only)        |
| DELETE | `/api/orders/<id>/`                | Delete order (admin only)            |
| GET    | `/api/order-count/<id>/`           | Count orders with same status        |
| GET    | `/api/completed-order-count/<id>/` | Count all completed orders           |
| GET    | `/api/reviews/`                    | List received reviews                |
| POST   | `/api/reviews/`                    | Submit a review                      |
| PATCH  | `/api/reviews/<id>/`               | Update own review                    |
| DELETE | `/api/reviews/<id>/`               | Delete own review                    |
| GET    | `/api/base-info/`                  | Public stats (offers, reviews, etc.) |

---

## 📗 API Endpunkte (Deutsch)

| Methode | Endpunkt                           | Beschreibung                            |
| ------- | ---------------------------------- | --------------------------------------- |
| POST    | `/api/registration/`               | Benutzer registrieren                   |
| POST    | `/api/login/`                      | Login und Token erhalten                |
| GET     | `/api/profile/<id>/`               | Nutzerprofil anzeigen                   |
| PATCH   | `/api/profile/<id>/`               | Eigenes Profil aktualisieren            |
| GET     | `/api/profiles/business/`          | Alle Business-Profile anzeigen          |
| GET     | `/api/profiles/customer/`          | Alle Kundenprofile anzeigen             |
| GET     | `/api/offers/`                     | Angebote auflisten (mit Filtern)        |
| POST    | `/api/offers/`                     | Neues Angebot mit Details erstellen     |
| GET     | `/api/offers/<id>/`                | Angebot mit Details anzeigen            |
| PATCH   | `/api/offers/<id>/`                | Angebot bearbeiten                      |
| GET     | `/api/offerdetails/<id>/`          | Einzelnes Angebotsdetail anzeigen       |
| GET     | `/api/orders/`                     | Eigene Bestellungen auflisten           |
| POST    | `/api/orders/`                     | Neue Bestellung aufgeben                |
| PATCH   | `/api/orders/<id>/`                | Status ändern (nur Business)            |
| DELETE  | `/api/orders/<id>/`                | Bestellung löschen (nur Admin)          |
| GET     | `/api/order-count/<id>/`           | Bestellungen mit gleichem Status zählen |
| GET     | `/api/completed-order-count/<id>/` | Alle abgeschlossenen zählen             |
| GET     | `/api/reviews/`                    | Bewertungen anzeigen (empfangen)        |
| POST    | `/api/reviews/`                    | Neue Bewertung schreiben                |
| PATCH   | `/api/reviews/<id>/`               | Eigene Bewertung ändern                 |
| DELETE  | `/api/reviews/<id>/`               | Eigene Bewertung löschen                |
| GET     | `/api/base-info/`                  | Öffentliche Plattform-Statistiken       |

---

## ⚙️ Setup (Local)

```bash
# 1. Clone the repo
git clone https://github.com/dein-user/coderr-backend.git
cd coderr-backend

# 2. Create virtual environment
python -m venv env
source env/bin/activate  # or .\env\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

---

## 🧪 Testing

```bash
python manage.py test
```

---

## 📦 Deployment (optional)

- Ready for Docker/Gunicorn (kann vorbereitet werden)
- `.env` Unterstützung für Settings wie DEBUG, SECRET_KEY etc.

---

## 👤 Test Instructions (Postman)

Please create two test users manually via Postman using:

```json
{
  "username": "GitHubCustomer",
  "email": "GitHub@mail.de",
  "password": "GitHubPassword",
  "repeated_password": "GitHubPassword",
  "type": "customer"
}
```

```json
{
  "username": "GitHubBusiness",
  "email": "GitHub@mail.de",
  "password": "GitHubPassword",
  "repeated_password": "GitHubPassword",
  "type": "business"
}
```

These accounts will allow testing both roles (customer + business) with token-based auth.

---

## ✍️ Author

Created by **Florian Irving**  
GitHub: [@BadPain](https://github.com/BadPain)  
Projektstatus: Wie immer, nie fertig. :D
