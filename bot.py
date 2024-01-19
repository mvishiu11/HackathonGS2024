from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Dict, List
import openai
from config import OpenAI_API_Key

app = FastAPI()

openai.api_key = OpenAI_API_Key

conversation_history: Dict[int, List[Dict]] = {}
conversation_length = 10  # Number of messages to keep in history

class UserInput(BaseModel):
    user_id: int
    message: str

@app.on_event("startup")
async def startup_event():
    print("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down...")

@app.post("/start/")
async def start(user_input: UserInput):
    user_id = user_input.user_id
    # Reset the conversation history for this user
    conversation_history[user_id] = []

    # Send a welcome message
    welcome_message = "Hi! I am your bot, ready to assist you. How can I help you today?"

    # Optionally, you can start with an initial message from the bot in the conversation history
    conversation_history[user_id].append({"role": "assistant", "content": welcome_message})
    
    return {"message": welcome_message}

@app.post("/message/")
async def process_message(user_input: UserInput):
    user_id = user_input.user_id
    user_message = user_input.message

    # Initialize conversation history if it's the first interaction
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Get conversation history for the user
    messages = conversation_history.get(user_id, [])
    if len(messages) >= 0 and len(messages) < conversation_length: 
        messages.append({"role": "user", "content": user_message})

    # Call GPT with the conversation history
    gpt_response = await ask_gpt("gpt-3.5-turbo", messages)

    # Save the latest response to history
    messages.append({"role": "assistant", "content": gpt_response})
    conversation_history[user_id] = messages

    return {"message": gpt_response}

async def ask_gpt(model, messages):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        error_message = str(e)
        if 'insufficient_quota' in error_message:
            return "I'm currently at my limit for AI responses. Please try again later."
        else:
            return f"Sorry, I encountered an error: {error_message}"