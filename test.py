from anyio import sleep
import openai
from openai import OpenAI
from config import OpenAI_API_Key
import asyncio

openai.api_key = OpenAI_API_Key


client = OpenAI(api_key=openai.api_key)

thread = client.beta.threads.create(
        messages=[  
        {
            "role": "user",
            "content": "Who are you?",
        }]
    )

async def ask_assistant():
    my_assistants = client.beta.assistants.list(order="desc", limit="20")
    assistant = [assistant for assistant in my_assistants.data if assistant.id == "asst_556gPLX8NXAjq27N5twckhjT"][0]
    print(assistant)
    
    run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
    )
    
    while(run.status != "completed"):
        run = client.beta.threads.runs.retrieve(
            run.id,
            thread_id=thread.id
        )
        print(run.status)
        await sleep(1)
    
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for message in messages.data[::-1]:
        print(message.content[0].text.value)

if __name__ == "__main__":
    asyncio.run(ask_assistant())
    
   
    
    