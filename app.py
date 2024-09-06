from flask import Flask, render_template, request, jsonify
import vertexai
from vertexai.language_models import ChatModel

app = Flask(__name__)

PROJECT_ID = "smart-impact-430905-t2"
LOCATION = "us-central1"

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

def create_session():
    try:
        chat_model = ChatModel.from_pretrained("gemini-1.5-flash-001")
        chat = chat_model.start_chat()
        return chat
    except Exception as e:
        print(f"Error creating chat session: {e}")
        return None

def response(chat, message):
    try:
        result = chat.send_message(message)
        return result.text
    except Exception as e:
        print(f"Error sending message: {e}")
        if "Quota exceeded" in str(e):
            return "Quota exceeded. Please try again later."
        return "Sorry, I couldn't process your request."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/palm2', methods=['GET', 'POST'])
def vertex_palm():
    user_input = ""
    if request.method == 'GET':
        user_input = request.args.get('user_input', '')
    elif request.method == 'POST':
        user_input = request.form.get('user_input', '')

    chat_model = create_session()
    if not chat_model:
        return jsonify(content="Failed to create chat session.")
    
    content = response(chat_model, user_input)
    return jsonify(content=content)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
