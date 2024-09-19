from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from flask_socketio import SocketIO, emit, join_room
import json
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder to save uploaded files
socketio = SocketIO(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

CHAT_DATA_FILE = 'chat_data.json'

def load_chat_data():
    if os.path.exists(CHAT_DATA_FILE):
        with open(CHAT_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_chat_data(data):
    with open(CHAT_DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room', methods=['POST'])
def create_room():
    username = request.form['username']
    room_name = request.form['room_name']
    
    chat_data = load_chat_data()
    
    if room_name not in chat_data:
        chat_data[room_name] = {'messages': [], 'users': []}

    if username not in chat_data[room_name]['users']:
        chat_data[room_name]['users'].append(username)

    save_chat_data(chat_data)
    return redirect(url_for('chat', room_name=room_name, username=username))

@app.route('/chat/<room_name>/<username>')
def chat(room_name, username):
    chat_data = load_chat_data()
    messages = chat_data.get(room_name, {}).get('messages', [])
    return render_template('chat.html', room_name=room_name, username=username, messages=messages)

@socketio.on('send_message')
def handle_send_message(data):
    room_name = data['room_name']
    username = data['username']
    message = data['message']
    
    chat_data = load_chat_data()
    chat_data[room_name]['messages'].append({'username': username, 'message': message})
    save_chat_data(chat_data)
    
    emit('receive_message', {'username': username, 'message': message}, room=room_name)

@socketio.on('send_file')
def handle_send_file(data):
    room_name = data['room_name']
    username = data['username']
    file_path = data['file_path']

    chat_data = load_chat_data()
    chat_data[room_name]['messages'].append({'username': username, 'file_path': file_path})
    save_chat_data(chat_data)
    
    emit('receive_file', {'username': username, 'file_path': file_path}, room=room_name)

@socketio.on('join')
def on_join(data):
    room_name = data['room_name']
    username = data['username']
    join_room(room_name)
    
    chat_data = load_chat_data()
    messages = chat_data.get(room_name, {}).get('messages', [])
    
    # Send only the loaded messages when a user joins
    emit('load_messages', messages, room=request.sid)
    emit('receive_message', {'username': 'System', 'message': f'{username} has joined the room.'}, room=room_name)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        return {'file_path': url_for('uploaded_file', filename=file.filename)}, 200  # Return the relative URL
    return {'error': 'File not uploaded'}, 400

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    socketio.run(app, debug=True)
