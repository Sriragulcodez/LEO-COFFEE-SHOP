
# Leo Coffee Shop ☕  

A beginner-friendly **full-stack coffee shop app** built with **FastAPI backend** and **Streamlit frontend**.  
Users can register, login, buy monthly passes, and get coffee with **real-time tracking** of remaining coffees.  

---

## Features
- User registration & login with **JWT authentication**  
- Monthly pass system (30 coffees/month)  
- Coffee consumption tracking  
- Clean and interactive **Streamlit frontend**  

---

## Project Structure

```

leo_coffee_shop/
├── backend/
│   └── main.py        # FastAPI backend
└── frontend/
└── app.py         # Streamlit frontend

````

---

## Step-by-Step Installation & Running Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-username>/leo_coffee_shop.git
cd leo_coffee_shop
````

### 2️⃣ Create a Python Virtual Environment (Recommended)

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3️⃣ Install Required Packages

```bash
pip install fastapi uvicorn pymongo passlib[bcrypt] python-jose streamlit requests
```

### 4️⃣ Start Backend (FastAPI)

```bash
uvicorn backend.main:app --reload
```

* Backend runs at: `http://127.0.0.1:8000`

### 5️⃣ Start Frontend (Streamlit)

```bash
streamlit run frontend/app.py
```

* Opens the Streamlit app in your default browser

---

## Usage Steps

1. **Register a New User**

   * Go to the "Register" page in the sidebar
   * Enter username and password → submit

2. **Login**

   * Go to the "Login" page
   * Enter username and password → submit
   * JWT token is stored automatically for further actions

3. **Buy / Renew Monthly Pass**

   * Go to the "Buy Pass" page
   * Click "Buy / Renew Pass" to get 30 coffees

4. **Get Coffee**

   * Go to the "Get Coffee" page
   * Click "Get Coffee" → remaining coffees update automatically
   * After 30 coffees → system will inform you to renew

---
