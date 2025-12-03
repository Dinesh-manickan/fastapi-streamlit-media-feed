# Fastapi-Streamlit-Media-Feed

A portfolio-ready full-stack Python project that implements a **mini social media feed** with:

- 🔐 Secure authentication (JWT)
- 📤 Image & video uploads to ImageKit
- 🧵 Async FastAPI backend using SQLite + SQLAlchemy
- 🎨 Streamlit frontend with a modern media-feed UI

This project showcases newly learned backend + frontend development skills with a real-world architecture.

---

## 🚀 Features

| Feature | Backend | Frontend |
|--------|:------:|:--------:|
| User auth (signup/login via JWT) | ✔️ | ✔️ |
| Upload image/video | ✔️ | ✔️ |
| ImageKit integration | ✔️ | ⚙️ |
| Social feed | ✔️ | ✔️ |
| Owner delete control | ✔️ | ✔️ |
| Async DB access | ✔️ | — |

---

## 🧰 Tech Stack

### Language & Tooling
- Python
- **uv** — Package + environment manager

### Backend
- FastAPI
- SQLAlchemy (async)
- aiosqlite
- fastapi-users (auth)
- Pydantic
- uvicorn

### Media / Storage
- ImageKit (CDN + uploads)

### Frontend
- Streamlit
- requests
- base64 / urllib.parse

---

## 🧠 What I Learned

This project helped me gain hands-on experience in:

- Building **async REST APIs** using FastAPI
- Secure **JWT authentication** with fastapi-users
- File upload pipelines using FastAPI + ImageKit
- Designing and querying async databases with SQLAlchemy models
- Building a **polished UI** in Python using Streamlit
- Using **uv** to manage venv + package installations
- Environment configuration via `.env` & `.env.example`

---

## 📁 Project Structure

```bash
.
├── main.py                  # Entry point -> runs FastAPI with Uvicorn
├── frontend.py              # Streamlit UI frontend
├── src/
│   ├── app.py               # FastAPI routes & server logic
│   ├── db.py                # SQLAlchemy models + async DB session
│   ├── users.py             # fastapi-users auth configuration
│   ├── images.py            # ImageKit upload client setup
│   ├── schemas.py           # Pydantic models for Post/User
├── .env                     # Private secrets (ignored in Git)
├── .env.example             # Safe template for contributors
├── README.md
├── pyproject.toml           # Managed using uv
└── requirements.txt         # (Optional)

Environment Setup

Create a `.env` file in the project root:

IMAGEKIT_PUBLIC_KEY=your_public_key_here
IMAGEKIT_PRIVATE_KEY=your_private_key_here
IMAGEKIT_URL_ENDPOINT=https://ik.imagekit.io/your_id
SECRET_KEY=your_fastapi_secret_key
DATABASE_URL=sqlite+aiosqlite:///./test.db

🛠 Installation & Running

Requires Python 3.11+ and uv
Install uv if needed:

pip install uv

1️⃣ Create & activate environment
uv venv
source .venv/bin/activate # macOS/Linux
.venv\Scripts\Activate.ps1 # Windows PowerShell

2️⃣ Install dependencies
uv sync

3️⃣ Run backend (FastAPI)
uv run main.py

Backend URL → http://localhost:8000

4️⃣ Run frontend (Streamlit)

Open new terminal (same venv):

streamlit run frontend.py

Frontend URL → http://localhost:8501

📌 Basic Usage

1️⃣ Register a user (via FastAPI docs or dedicated auth routes)
2️⃣ Login in the Streamlit sidebar
3️⃣ Upload an image or video + caption
4️⃣ View your posts in the feed
5️⃣ Delete only your own posts 🔒

🚧 Future Improvements

👍 Like & comment system

🧑‍🤝‍🧑 User profile page + avatar upload

🔄 Infinite scroll feed

📱 Mobile-responsive layout

🧪 Automated tests (pytest)

🌐 Deployment: Railway / Render / Fly.io + Streamlit Cloud

This README **looks professional**, communicates value, and helps recruiters/devs run your project **without hand-holding**.
### Thanks
