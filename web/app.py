from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(file))))

from core.metacontrol.memory import load_memory
from core.network.discovery import get_nodes
from core.compiler.cache import cache_stats
from core.life.scheduler import _scheduler
from core.orchestrator.distributed import _distributed

app = Flask(name, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/memory')
def memory_view():
    return render_template('memory.html')

@app.route('/nodes')
def nodes_view():
    return render_template('nodes.html')

@app.route('/tasks')
def tasks_view():
    return render_template('tasks.html')

@app.route('/compiler')
def compiler_view():
    return render_template('compiler.html')

# API endpoints
@app.route('/api/memory')
def api_memory():
    memory = load_memory()
    return jsonify(memory)

@app.route('/api/nodes')
def api_nodes():
    nodes = get_nodes()
    return jsonify({
        'nodes': nodes,
        'count': len(nodes)
    })

@app.route('/api/cache/stats')
def api_cache_stats():
    return jsonify(cache_stats())

@app.route('/api/scheduler/tasks')
def api_scheduler_tasks():
    if hasattr(_scheduler, 'tasks'):
        tasks = [
            {
                'id': t[1] if len(t) > 1 else 'unknown',
                'time': t[0],
                'command': t[2] if len(t) > 2 else 'unknown'
            } for t in _scheduler.tasks
        ]
        return jsonify({'tasks': tasks})
    return jsonify({'tasks': []})

@app.route('/api/distributed/stats')
def api_distributed_stats():
    return jsonify({
        'node_id': getattr(_distributed, 'node_id', 'unknown'),
        'running': getattr(_distributed, 'running', False),
        'node_tasks': dict(getattr(_distributed, 'node_tasks', {}))
    })

@app.route('/api/execute', methods=['POST'])
def api_execute():
    data = request.json
    command = data.get('command', '')
    mode = data.get('mode', 'local')
    
    if mode == 'distributed':
        from core.orchestrator.distributed import execute_distributed
        result = execute_distributed(command)
    else:
        from core.orchestrator.engine import run_orchestrator
        result = run_orchestrator({"command": command}, sync=False)
    
    return jsonify(result)

@app.route('/static/')
def static_files(filename):
    return send_from_directory('static', filename)

if name == 'main':
    print("Starting Jarvis Web UI on http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=True)