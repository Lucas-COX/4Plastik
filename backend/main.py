from typing import Union, List
import asyncio
import dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel
import queue
import pickle
import numpy as np
import sqlite3
import os

if "MODEL_PATH" not in os.environ.keys():
    dotenv.load_dotenv()

app = FastAPI()

# Define a simple queue to hold incoming messages
message_queue = queue.Queue()

# List to hold processed messages
processed_messages: List[dict] = []

model_path = os.environ.get("MODEL_PATH")
data_path = os.path.join(os.path.dirname(__file__), 'data/messages.db')

# Load the trained model (assuming the model is saved as 'suicide_model.pkl')
with open(model_path, 'rb') as model_file:
    suicide_model = pickle.load(model_file)

# Define the incoming request model
class Message(BaseModel):
    account: str
    content: str
    social: str

# Endpoint to receive messages and add them to the queue
@app.post("/add-message")
async def add_message(message: Message):
    message_queue.put(message)
    return {"status": "Message added to queue"}

# Function to process messages from the queue asynchronously
async def process_queue():
    conn = sqlite3.connect(data_path)
    cursor = conn.cursor()
    while True:
        if not message_queue.empty():
            message = message_queue.get()
            
            # Preprocess the message content for the model
            # Note: Actual preprocessing steps depend on how the model was trained
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

# Endpoint to get all processed messages
@app.get("/get-processed-messages")
async def get_processed_messages():
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
