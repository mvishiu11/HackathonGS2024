from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, Dict, List
import openai
from config import OpenAI_API_Key
from config import assistant_id
from openai import OpenAI
import asyncio
import copy
import logging
from utils.logger import CustomFormatter

app = FastAPI()

openai.api_key = OpenAI_API_Key

# Logger setup
log_level = 'INFO'
logger = logging.getLogger(__name__)
logger.setLevel(log_level)
ch = logging.StreamHandler()
ch.setLevel(log_level)
ch.setFormatter(CustomFormatter())
logger.addHandler(ch)

conversation_history = {}
conversation_length = 10  # Number of messages to keep in history

use_assistant = True  # Set to True to use your assistant, False to use GPT-3 directly

class UserInput(BaseModel):
    user_id: int
    message: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    logger.info("Starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down...")

@app.post("/start/")
async def start(user_input: UserInput):
    user_id = user_input.user_id
    # Reset the conversation history for this user
    conversation_history[user_id] = []

    # Send a welcome message
    welcome_message = "Hi! I am your bot, ready to assist you. How can I help you today?"

    # Optionally, you can start with an initial message from the bot in the conversation history
    conversation_history[user_id].append({"role": "user", "content": "Assistant: " + welcome_message})
    
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
    if len(messages) >= 0 and len(messages) < conversation_length and user_message: 
        messages.append({"role": "user", "content": user_message})

    # Choose between GPT and your assistant based on the conversation
    if use_assistant:  # Replace this with actual condition to choose assistant
        logger.info("Using assistant")
        # gpt_response = await ask_assistant(user_id)  # This needs the appropriate thread id or modification
    else:
        logger.info("Using GPT")
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


@app.post("/assistant/")        
async def assistant(user_input: UserInput) -> None:
    client = OpenAI(api_key=openai.api_key)
    user_id = user_input.user_id
    user_message = "User: " + user_input.message

    # Initialize conversation history if it's the first interaction
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Get conversation history for the user
    messages = []
    if len(messages) < conversation_length: 
        messages.append({"role": "user", "content": user_message})

    logger.info(messages)
    
    # Get thread id for the user
    thread = client.beta.threads.create(
        messages=messages
    )
    
    # Call GPT with the conversation history
    gpt_response = await ask_assistant(thread.id)
    if ("Assistant: " in gpt_response):
        assistant_reponse = copy.deepcopy(gpt_response)
        gpt_response = gpt_response.replace("Assistant: ", "")
    else:
        assistant_reponse = "Assistant: " + gpt_response

    # Save the latest response to history
    messages.append({"role": "user", "content": assistant_reponse})
    conversation_history[user_id] = messages
    
    logger.info(gpt_response)

    return {"message": gpt_response}


async def ask_assistant(thread_id):
    client = OpenAI(api_key=openai.api_key)
    my_assistants = client.beta.assistants.list(order="desc", limit="20")
    assistant = [assistant for assistant in my_assistants.data if assistant.id == assistant_id][0]
    
    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant.id,
    )
    
    while(run.status != "completed"):
        run = client.beta.threads.runs.retrieve(
            run.id,
            thread_id=thread_id
        )
        logger.info(run.status)
        if(run.status == "failed"):
            logger.warning("Run failed")
            return "Sorry, I encountered an error. Please try again later."
        await asyncio.sleep(1)
    
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    logger.info(messages.data[0].content[0].text.value)
    return messages.data[0].content[0].text.value