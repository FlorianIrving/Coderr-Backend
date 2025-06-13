# Coderr Backend

Coderr is the backend service for a freelance collaboration platform.  
It is built with Django and Django REST Framework and provides endpoints for authentication, offers, orders, reviews, and statistical base information.

---

## 🚀 Getting Started

### ✅ Prerequisites

- Python 3.10+
- pip
- (Optional) Virtualenv
- PostgreSQL or SQLite3 (default)

### 📦 Installation

```bash
# Clone the repository
git clone https://github.com/your-username/coderr-backend.git
cd coderr-backend

# Create and activate virtual environment
python -m venv env
source env/bin/activate  # Linux/macOS
# OR
env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# (Optional) Create a superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

---

## 🔐 Authentication

This project uses JWT (JSON Web Tokens) for secure API access.

- Obtain token:
  `POST /api/token/`  
- Refresh token:
  `POST /api/token/refresh/`

---

## 🧱 API Structure

| Area         | Description                               |
|--------------|-------------------------------------------|
| `/api/auth/` | Registration, login, profile              |
| `/api/offers/` | Offer creation, detail levels           |
| `/api/orders/` | Order placement and management          |
| `/api/reviews/` | Review creation, update, and deletion |
| `/api/base-info/` | Public platform stats (no auth)     |

---

## 📊 `/api/base-info/`

Returns live public metrics of the platform:

```json
{
  "review_count": 10,
  "average_rating": 4.6,
  "business_profile_count": 45,
  "offer_count": 150
}
```

- ✅ No authentication required
- ✅ Rounded to one decimal
- ✅ Live aggregated data from the database

---

## ⚙️ Project-Specific Notes

- Reviews are managed using **separate models** for POST/GET and PATCH/DELETE.
- The `reviewer` is automatically set via `request.user` and cannot be spoofed.
- Reviews can only be updated or deleted by the original reviewer.
- The `BaseInfoView` is public and reflects platform-wide live data.
- All business users are determined via their related `UserProfile` (`profile__type = "business"`).

---

## 📁 Technologies Used

- Django 4.x
- Django REST Framework
- djangorestframework-simplejwt
- Python 3.10+
- PostgreSQL (or SQLite for development)

---

## 📮 Contact

Developed by **Florian Irving**  
GitHub: [@BadPain](https://github.com/BadPain)
