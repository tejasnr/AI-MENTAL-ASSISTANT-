import os
import requests
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)  # For session management

# Initialize Flask-SocketIO for real-time communication
socketio = SocketIO(app)

# Retrieve the API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Placeholder for the chat object connected to Google Gemini API
class ChatAPI:
    def __init__(self):
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"  # Replace with actual Google Gemini API endpoint

    def send_message(self, message):
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }

        # Define the payload with the user message
        payload = {
            "input": message,
            # Add any additional parameters that the Gemini API requires
        }

        try:
            # Make the request to the Google Gemini API
            response = requests.post(self.api_url, json=payload, headers=headers)

            # Check for a successful response
            if response.status_code == 200:
                data = response.json()
                return data['response']  # Modify according to the API response structure
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error connecting to API: {str(e)}"

# Instantiate the chat API class
chat = ChatAPI()

# Pre-defined instructions for the chatbot
prompt_instructions = (
    "You are a compassionate and skilled mental health assistant, focused on providing a safe and comforting space for users experiencing stress, anxiety, or emotional distress. "
    "Your role is to offer empathetic, patient, and non-judgmental responses that make the user feel heard and understood. "
    "Always prioritize active listening and respond in a way that validates their feelings, reflecting understanding and kindness. "
    "Gently offer practical coping strategies and encouragement tailored to their needs, but avoid any medical or diagnostic advice. "
    "Use a calm, reassuring tone, choosing comforting words to foster trust and safety. "
    "Your goal is to make the user feel supported, understood, and less alone in their struggles. "
    "Avoid using emojis, slang, or informal language in your responses."
)

# Function to format and send a message to the API
def send_message_with_instructions(chat, prompt_instructions, user_prompt):
    full_prompt = f"{prompt_instructions}\n\n{user_prompt}"
    return chat.send_message(full_prompt)

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

# SocketIO event handling for real-time chat
@socketio.on('user_message')
def handle_user_message(message):
    # Send the user's message to the API and get the assistant's response
    response = send_message_with_instructions(chat, prompt_instructions, message)
    # Send the assistant's response back to the user
    emit('assistant_message', response)

# Main entry point for running the Flask app
if __name__ == '__main__':
    socketio.run(app, debug=True)
