from flask import Flask, render_template, request, jsonify, Blueprint
from flask_socketio import SocketIO

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
main = Blueprint('main', __name__)
socketio = SocketIO()

@main.route('/')
def index():
    return render_template('index.html')

@socketio.on('update_message')
def update_message(new_message):
    global message
    message = new_message
    socketio.emit('message_updated', message)

@main.route('/update_message', methods=['POST'])
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
    app = create_app()
    socketio.init_app(app)
    socketio.run(app, debug=False, host='0.0.0.0')