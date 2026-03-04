from flask import Flask, request, jsonify
import threading
import uuid
import time

app = Flask(__name__)
tasks = {}

@app.route('/execute', methods=['POST'])
def execute():
    data = request.json
    task_id = str(uuid.uuid4())[:8]
    print(f"[Server] Task {task_id}: {data}")
    
    tasks[task_id] = {'status': 'pending'}
    
    def run():
        time.sleep(1)
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['result'] = {'ok': True}
    
    threading.Thread(target=run, daemon=True).start()
    return jsonify({'status': 'accepted', 'task_id': task_id})

@app.route('/result/<task_id>')
def result(task_id):
    return jsonify(tasks.get(task_id, {'error': 'not found'}))

@app.route('/stats')
def stats():
    return jsonify({'tasks': len(tasks), 'status': 'ok'})

@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("Server starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
