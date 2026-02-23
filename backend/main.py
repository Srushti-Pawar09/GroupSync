from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import psycopg2
import os
from passlib.context import CryptContext
from jose import JWTError, jwt
import datetime
from google import genai

# -----------------------------
# App setup
# -----------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Environment
# -----------------------------
DATABASE_URL = os.getenv("DATABASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

client = genai.Client(api_key=GEMINI_API_KEY)

# -----------------------------
# DB connection helper
# -----------------------------
def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

# -----------------------------
# Auth setup
# -----------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

import hashlib

def hash_password(password: str) -> str:
    if len(password.encode("utf-8")) > 72:
        password = password[:72]
    return pwd_context.hash(password)
def verify_password(password: str, hashed: str) -> bool:
    if len(password.encode("utf-8")) > 72:
        password = password[:72]
    return pwd_context.verify(password, hashed)

def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# -----------------------------
# Routes
# -----------------------------

@app.get("/")
def home():
    return {"message": "GroupSync Backend is running"}

# -------- Register --------
@app.post("/register")
def register(payload: dict):
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    conn = get_db_connection()
    cursor = conn.cursor()

    hashed = hash_password(password)

    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, hashed)
        )
        conn.commit()
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    conn.close()
    return {"message": "User created successfully"}
# -------- Login --------
@app.post("/login")
def login(payload: dict):
    username = payload.get("username")
    password = payload.get("password")

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password required")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT password_hash FROM users WHERE username=%s",
        (username,)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(password, user[0]):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token(username)

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# -------- Get Messages --------
@app.get("/messages/{group_id}")
def get_messages(group_id: str, username: str = Depends(get_current_user)):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT username, message, role FROM messages WHERE group_id=%s ORDER BY created_at",
        (group_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    messages = [
        {"username": r[0], "message": r[1], "role": r[2]}
        for r in rows
    ]

    return {"messages": messages}

# -------- Chat --------
@app.post("/chat")
def chat(payload: dict, username: str = Depends(get_current_user)):
    group_id = payload["group_id"]
    message = payload["message"]

    conn = get_db_connection()
    cursor = conn.cursor()

    # Create group if not exists
    cursor.execute(
        "INSERT INTO groups (id) VALUES (%s) ON CONFLICT DO NOTHING",
        (group_id,)
    )

    # Save user message
    cursor.execute(
        "INSERT INTO messages (group_id, username, message, role) VALUES (%s, %s, %s, %s)",
        (group_id, username, message, "user")
    )
    conn.commit()

    # Fetch conversation
    cursor.execute(
        "SELECT username, message, role FROM messages WHERE group_id=%s ORDER BY created_at",
        (group_id,)
    )
    history = cursor.fetchall()

    conversation_text = ""
    for h in history:
        conversation_text += f"{h[0]} ({h[2]}): {h[1]}\n"

    prompt = f"""
You are a helpful travel planning assistant in a group chat.
Respond naturally and helpfully.

Conversation:
{conversation_text}
"""

    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=prompt
    )

    reply = response.text

    # Save assistant reply
    cursor.execute(
        "INSERT INTO messages (group_id, username, message, role) VALUES (%s, %s, %s, %s)",
        (group_id, "assistant", reply, "assistant")
    )
    conn.commit()
    conn.close()

    return {"reply": reply}