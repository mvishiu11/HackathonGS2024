from fastapi.testclient import TestClient
from bot import app

client = TestClient(app)

def test_start():
    response = client.post("/start/", json={"user_id": 1, "message": "Hello!"})
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "Hi! I am your bot, ready to assist you. How can I help you today?"}

def test_process_message():
    # Starting a new conversation
    client.post("/start/", json={"user_id": 1})
    
    # Sending a message
    user_message = "Hello, who are you?"
    response = client.post("/assistant/", json={"user_id": 1, "message": user_message})
    
    print(response.json())
    
    assert response.status_code == 200
    assert "message" in response.json()

    # This part is commented out because the actual response depends on the OpenAI model's response
    # assert response.json() == {"message": "Expected GPT-3 response"}
    
if __name__ == "__main__":
    test_start()
    test_process_message()