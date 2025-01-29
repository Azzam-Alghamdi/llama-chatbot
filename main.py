from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
from bot import generate_ai_response
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Secret key for session management

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    user_message = request.form['message']
    timestamp = datetime.now().strftime('%H:%M:%S')

    # Initialize session-specific messages if not present
    if 'messages' not in session:
        session['messages'] = []

    # Add user message to session
    session['messages'].append({
        'text': user_message,
        'time': timestamp,
        'sender': 'user'
    })

    # Generate and add bot response using AI
    bot_response = generate_ai_response(user_message)
    session['messages'].append({
        'text': bot_response,
        'time': datetime.now().strftime('%H:%M:%S'),
        'sender': 'bot'
    })

    session.modified = True  # Ensure the session is updated

    return jsonify({'status': 'success'})

@app.route('/messages')
def get_messages():
    return jsonify({'messages': session.get('messages', [])})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
