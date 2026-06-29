import logging
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, File, Header, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from Backend import ai, auth, db

BASE_DIR = Path(__file__).resolve().parents[1]
app = FastAPI()
app.mount("/static", StaticFiles(directory=str(BASE_DIR.joinpath("Frontend"))), name="static")

logger = logging.getLogger("flower_shop")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def get_current_email(
    authorization: str | None = Header(None, alias="Authorization"),
    email: str | None = Header(None, alias="X-User-Email"),
) -> str:
    if not authorization or not email:
        raise HTTPException(status_code=401, detail="Missing auth credentials")
    if authorization.startswith("Bearer "):
        token = authorization.split("Bearer ", 1)[1].strip()
    else:
        token = authorization.strip()
    if not auth.get_email_from_token(token, email):
        raise HTTPException(status_code=401, detail="Invalid token")
    return email


@app.on_event("startup")
def startup_event() -> None:
    db.initialize_database()
    logger.info("Flower Shop database initialized")


@app.get("/", response_class=HTMLResponse)
def homepage() -> HTMLResponse:
    return HTMLResponse(BASE_DIR.joinpath("Frontend", "index.html").read_text(encoding="utf-8"))


@app.post("/api/signup")
def signup(payload: dict[str, str]) -> dict[str, str]:
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    password_hash = auth.hash_password(password)
    try:
        db.execute(
            "INSERT INTO customers (name, email, password_hash) VALUES (?, ?, ?)",
            (email.split("@")[0], email, password_hash),
        )
    except Exception as exc:
        logger.warning("Signup failed: %s", exc)
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "Signup successful"}


@app.post("/api/login")
def login(payload: dict[str, str]) -> dict[str, str]:
    email = payload.get("email", "").strip().lower()
    password = payload.get("password", "")
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    user = db.query_one("SELECT email, password_hash FROM customers WHERE email = ?", (email,))
    if not user or not auth.validate_login(email, password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = auth.create_token(email)
    return {"token": token, "email": email}


@app.post("/api/chat")
def chat(payload: dict[str, str], current_email: str = Depends(get_current_email)) -> dict[str, Any]:
    question = payload.get("question", "").strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    route = classify_query(question)
    logger.info("Chat request from %s route=%s question=%s", current_email, route, question)

    if route == "rag":
        return ai.rag_search(question)
    if route == "text2sql":
        return ai.count_low_stock() if "low stock" in question.lower() else ai.find_promotions()
    return {"answer": "I can only answer Flower Shop questions about product details, care instructions, stock, and promotions.", "source": "direct", "confidence": 0.8}


@app.post("/api/upload")
def upload_image(
    file: UploadFile = File(...),
    current_email: str = Depends(get_current_email),
) -> dict[str, str]:
    if file.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        raise HTTPException(status_code=400, detail="Image must be PNG or JPEG")
    contents = file.file.read(2_000_000)
    if len(contents) >= 2_000_000:
        raise HTTPException(status_code=400, detail="Image too large")
    logger.info("Image upload received from %s file=%s size=%d", current_email, file.filename, len(contents))
    return {"message": "Upload received", "filename": file.filename}


@app.get("/api/status")
def status() -> dict[str, Any]:
    healthy_db = db.check_connection()
    return {
        "status": "ok" if healthy_db else "unhealthy",
        "database": "connected" if healthy_db else "disconnected",
        "version": "1.0.0",
    }


def classify_query(question: str) -> str:
    keywords_rag = ["what", "describe", "tell me", "how do", "how to", "care", "when", "why"]
    keywords_sql = ["how many", "which", "list", "count", "total", "price", "stock", "available"]
    lower = question.lower()
    if any(keyword in lower for keyword in keywords_sql):
        return "text2sql"
    if any(keyword in lower for keyword in keywords_rag):
        return "rag"
    return "unknown"


@app.get("/chat", response_class=HTMLResponse)
def chat_page() -> HTMLResponse:
    return HTMLResponse(BASE_DIR.joinpath("Frontend", "chat.html").read_text(encoding="utf-8"))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("Backend.app:app", host="127.0.0.1", port=8000, log_level="info")
