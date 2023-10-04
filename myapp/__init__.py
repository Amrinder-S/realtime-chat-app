from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO

def create_app():
	app = Flask(__name__)
	return app
socketio = SocketIO(create_app())

@create_app().route('/')
def index():
    return render_template('index.html')

@socketio.on('update_message')
def update_message(new_message):
    global message
    message = new_message
    socketio.emit('message_updated', message)

@create_app().route('/update_message', methods=['POST'])
def update_message_post():
    global message
    new_message = request.form.get('new_message')
    if new_message:
        message = new_message
        socketio.emit('message_updated', message)
        return jsonify({"message": "Message updated successfully"})
    else:
        return jsonify({"error": "New message not provided"}), 400


if __name__ == '__main__':
    socketio.run(create_app(), debug=False, host='0.0.0.0')
