from typing import Union, List
import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
import queue
import pickle
import numpy as np

app = FastAPI()

# Define a simple queue to hold incoming messages
message_queue = queue.Queue()

# List to hold processed messages
processed_messages: List[dict] = []

# Load the trained model (assuming the model is saved as 'suicide_model.pkl')
with open('suicide_model.pkl', 'rb') as model_file:
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
    while True:
        if not message_queue.empty():
            message = message_queue.get()
            
            # Preprocess the message content for the model
            # Note: Actual preprocessing steps depend on how the model was trained
            input_data = np.array([message.content])
            
            # Execute model to get the score
            score = suicide_model.predict(input_data)[0]
            
            # Store the processed message and its score
            processed_messages.append({
                "account": message.account,
                "content": message.content,
                "social": message.social,
                "score": score
            })
            
            print(f"Processed message from {message.account} on {message.social}: \"{message.content}\", Score: {score}")
        await asyncio.sleep(1)

# Background task to process the queue
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(process_queue())

# Endpoint to get all processed messages
@app.get("/get-processed-messages")
async def get_processed_messages():
    return {"processed_messages": processed_messages}

# Default endpoint
@app.get("/")
def read_root():
    return {"Hello": "World"}
