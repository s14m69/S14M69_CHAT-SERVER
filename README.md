# 🗨️ Flask Chat Application

A real-time chat application built with **Flask** and **Flask-SocketIO**. This app allows users to create chat rooms, send messages, and share files seamlessly.

## 🚀 Features

- **Create and Join Chat Rooms**: Easily create new rooms or join existing ones.
- **Real-Time Messaging**: Communicate instantly with other users.
- **File Uploads**: Share files directly in the chat.
- **Message History**: Chat history is stored and retrievable.
- **User Notifications**: Receive notifications when users join.

## 📋 Requirements

- Python 3.6+
- Flask
- Flask-SocketIO

## 📥 Installation

### Clone the Repository

To get started, clone the repository to your local machine:

```bash
git clone https://github.com/s14m69/S14M69_CHAT-SERVER.git
cd S14M69_CHAT-SERVER
pip install Flask Flask-SocketIO
mkdir uploads
python index.py
```
## ⚙️ Configuration

### Important Configuration Variables

- **SECRET_KEY**: Set this in `app.config['SECRET_KEY']` for session management and security. It is crucial for protecting user sessions.

- **UPLOAD_FOLDER**: Define the folder path where uploaded files will be stored. The default is `uploads/`.

## 🌐 Endpoints

### Main Routes

- **`/`**:
  - **GET**: Renders the main page for creating or joining a room.

- **`/create_room`**:
  - **POST**: Creates a new chat room and adds the user to it.

- **`/chat/<room_name>/<username>`**:
  - **GET**: Renders the chat page for the specified room and user.

- **`/upload`**:
  - **POST**: Handles file uploads and saves them to the server.

- **`/uploads/<path:filename>`**:
  - **GET**: Serves uploaded files.

## 📡 Real-time Messaging

Using **Flask-SocketIO**, the application supports real-time messaging, ensuring that messages and files are instantly available to all users in a room.

## 📝 Usage

1. Open your web browser and navigate to `http://localhost:5000`.
2. Enter a username and room name to create or join a chat room.
3. Start chatting and sharing files!

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or discover bugs, please create an issue or submit a pull request.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## 🙏 Acknowledgements

- **Flask** - A micro web framework for Python.
- **Flask-SocketIO** - Enables real-time communication in Flask applications.

