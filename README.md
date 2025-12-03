Project Set-up

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
