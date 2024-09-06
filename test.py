import time
import vertexai
from vertexai.generative_models import GenerativeModel

PROJECT_ID = "smart-impact-430905-t2"
LOCATION = "us-central1"

def initialize_vertexai():
    vertexai.init(project=PROJECT_ID, location=LOCATION)

def create_session():
    initialize_vertexai()
    try:
        chat_model = GenerativeModel("gemini-1.5-flash-001")
        chat = chat_model.start_chat()
        return chat
    except Exception as e:
        print(f"Error creating chat session: {e}")
        return None

def response(chat, message):
    parameters = {}  # Remove parameters as they are not supported
    try:
        result = chat.send_message(message)  # Send message without parameters
        return result.text
    except Exception as e:
        if "Quota exceeded" in str(e):
            print("Quota exceeded. Please try again later.")
            time.sleep(60)  # Wait for a minute before retrying
        else:
            print(f"Error sending message: {e}")
        return "Sorry, I couldn't process your request."

def run_chat():
    chat_model = create_session()
    if not chat_model:
        print("Failed to create chat session.")
        return

    print("Chat Session created. Type 'exit' or 'quit' to end the chat.")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        
        content = response(chat_model, user_input)
        print(f"AI: {content}")

if __name__ == '__main__':
    run_chat()
