from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import threading
import uuid
from core.managers import BotManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sim_secret'
socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    return render_template('console.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    amount = int(data.get('amount', 1))
    
    # Hard cap for simulation safety
    if amount > 10: amount = 10
    
    task_id = str(uuid.uuid4())
    manager = BotManager(task_id, socketio)
    
    thread = threading.Thread(target=manager.run_batch, args=(amount,))
    thread.start()
    
    return jsonify({"status": "started", "id": task_id})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')