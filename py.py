from flask import Flask, request, jsonify
from urllib.parse import unquote
from datetime import datetime

app = Flask(__name__)

# In-memory storage for chat messages
rooms = {}

# Route for receiving messages
@app.route('/room=<room>/author=<author>/msg=<msg>')
def send_message(room, author, msg):
    # URL-decode each part
    room = unquote(room)
    author = unquote(author)
    msg = unquote(msg)

    # Add timestamp
    timestamp = datetime.utcnow().isoformat()

    if room not in rooms:
        rooms[room] = []

    rooms[room].append({"author": author, "msg": msg, "timestamp": timestamp})

    return "OK", 200

# Endpoint to fetch messages in a room
@app.route('/get')
def get_messages():
    room = request.args.get('room')
    if not room or room not in rooms:
        return jsonify([])

    # Return the latest messages (top 6 newest)
    latest = rooms[room][-6:]  # last 6 messages
    return jsonify(latest)

if __name__ == '__main__':
    app.run(port=24864)
