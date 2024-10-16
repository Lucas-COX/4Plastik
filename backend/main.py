from typing import Annotated, Union
import asyncio
import dotenv
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
import pickle
import numpy as np
import sqlite3
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
import jwt
import bcrypt
import os

if "MODEL_PATH" not in os.environ.keys():
    dotenv.load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",   
    "http://127.0.0.1:5173"    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],  
)

# Define an asyncio queue to hold incoming messages
message_queue = asyncio.Queue()

model_path = os.environ.get("MODEL_PATH")
data_path = os.path.join(os.path.dirname(__file__), 'data/messages.db')

with open(model_path, 'rb') as model_file:
    suicide_model = pickle.load(model_file)
    
# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
SECRET_KEY = "testsecretkey"
ALGORITHM = "HS256"

# Define the incoming request model
class Message(BaseModel):
    account: str
    content: str
    social: str

# Verify user credentials against the 'users' table
def verify_user(email: str, password: str) -> bool:
    conn = sqlite3.connect(data_path)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    if user is None:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8'))

# Verify API key against the 'api_keys' table
def verify_api_key(key: str) -> bool:
    conn = sqlite3.connect(data_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM api_keys WHERE key = ?", (key,))
    api_key = cursor.fetchone()
    conn.close()
    return api_key is not None

class LoginRequest(BaseModel):
    username: str
    password: str

@app.post("/token")
async def login_for_access_token(login_request: LoginRequest):
    if not verify_user(login_request.username, login_request.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = jwt.encode({"sub": login_request.username}, SECRET_KEY, algorithm=ALGORITHM)
    print(token)
    return {"access_token": token, "token_type": "bearer"}

# Endpoint to receive messages and add them to the queue (protected by API key)
@app.post("/add-message")
async def add_message(message: Message, token: str = Depends(oauth2_scheme)):
    if not verify_api_key(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    await message_queue.put(message)
    return {"status": "Message added to queue"}

# Function to process messages from the queue asynchronously
async def process_queue():
    conn = sqlite3.connect(data_path)
    cursor = conn.cursor()
    while True:
        if not message_queue.empty():
            message = await message_queue.get()
            
            # Preprocess the message content for the model
            input_data = np.array([message.content])
            
            # Execute model to get the score
            score = suicide_model.predict(input_data)[0]
            
            # Store the processed message and its score
            cursor.execute('''
                INSERT INTO messages (account, content, social, score) 
                VALUES (?, ?, ?, ?)
            ''', (message.account, message.content, message.social, score))
            conn.commit()
            
            print(f"Processed message from {message.account} on {message.social}: \"{message.content}\", Score: {score}")
        await asyncio.sleep(1)
    conn.close()

# Background task to process the queue
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_queue())
    
def user_exists(email):
    conn = sqlite3.connect(data_path)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# Endpoint to get all processed messages (protected by user authentication)
@app.get("/get-processed-messages")
async def get_processed_messages(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if email is None or not user_exists(email):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    conn = sqlite3.connect(data_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM messages")
    rows = cursor.fetchall()
    conn.close()
    
    processed_messages = [
        {"id": row[0], "account": row[1], "content": row[2], "social": row[3], "score": row[4]} 
        for row in rows
    ]
    return {"processed_messages": processed_messages}

# Default endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}
