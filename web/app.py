from flask import Flask, render_template, jsonify, request, send_from_directory
import json
import os
import sys

# Абсолютный путь к корневой директории
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

print(f"Root directory: {ROOT_DIR}")
print(f"Python path: {sys.path[0]}")

# Проверяем наличие core модулей
core_metacontrol_path = os.path.join(ROOT_DIR, 'core', 'metacontrol')
core_network_path = os.path.join(ROOT_DIR, 'core', 'network')
core_compiler_path = os.path.join(ROOT_DIR, 'core', 'compiler')

print(f"Core metacontrol exists: {os.path.exists(core_metacontrol_path)}")
print(f"Core network exists: {os.path.exists(core_network_path)}")
print(f"Core compiler exists: {os.path.exists(core_compiler_path)}")

# Импортируем core модули
CORE_AVAILABLE = False
try:
    from core.metacontrol.memory import load_memory
    from core.network.discovery import get_nodes
    from core.compiler.cache import cache_stats
    print("✓ Core modules imported successfully")
    CORE_AVAILABLE = True
except ImportError as e:
    print(f"✗ Core import error: {e}")
    
    # Пробуем альтернативный импорт
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "memory", 
            os.path.join(ROOT_DIR, "core", "metacontrol", "memory.py")
        )
        if spec:
            memory = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(memory)
            load_memory = memory.load_memory
            print("✓ memory.py loaded via spec")
            CORE_AVAILABLE = True
    except Exception as e2:
        print(f"✗ Alternative import failed: {e2}")

app = Flask(__name__, static_folder='static', template_folder='templates')

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

@app.route('/api/status')
def api_status():
    return jsonify({
        "status": "running", 
        "version": "3.0.1",
        "core_available": CORE_AVAILABLE,
        "root_dir": ROOT_DIR
    })

@app.route('/api/memory')
def api_memory():
    if not CORE_AVAILABLE:
        return jsonify({"error": "Core modules not available", "experiences": [], "best_sequences": {}, "patterns": {}})
    try:
        if 'load_memory' in globals():
            memory = load_memory()
            return jsonify(memory)
        else:
            return jsonify({"error": "load_memory not defined", "experiences": []})
    except Exception as e:
        return jsonify({"error": str(e), "experiences": []})

@app.route('/api/nodes')
def api_nodes():
    if not CORE_AVAILABLE:
        return jsonify({"nodes": {}, "count": 0})
    try:
        if 'get_nodes' in globals():
            nodes = get_nodes()
            return jsonify({'nodes': nodes, 'count': len(nodes)})
        else:
            return jsonify({"nodes": {}, "count": 0})
    except Exception as e:
        return jsonify({"nodes": {}, "count": 0, "error": str(e)})

@app.route('/api/cache/stats')
def api_cache_stats():
    if not CORE_AVAILABLE:
        return jsonify({"hits": 0, "misses": 0, "size": 0, "hit_rate": 0})
    try:
        if 'cache_stats' in globals():
            return jsonify(cache_stats())
        else:
            return jsonify({"hits": 0, "misses": 0, "size": 0, "hit_rate": 0})
    except Exception as e:
        return jsonify({"hits": 0, "misses": 0, "size": 0, "hit_rate": 0, "error": str(e)})

@app.route('/api/execute', methods=['POST'])
def api_execute():
    data = request.json
    command = data.get('command', '')
    mode = data.get('mode', 'local')
    
    if not CORE_AVAILABLE:
        return jsonify({"status": "demo", "message": f"Demo execution: {command}", "mode": mode})
    
    try:
        if mode == 'distributed':
            # Импортируем здесь, чтобы избежать циклических зависимостей
            from core.orchestrator.distributed import execute_distributed
            result = execute_distributed(command)
        else:
            from core.orchestrator.engine import run_orchestrator
            result = run_orchestrator({"command": command}, sync=False)
        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

@app.route('/api/test')
def api_test():
    return jsonify({
        "message": "API is working",
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "core_available": CORE_AVAILABLE,
        "root_dir": ROOT_DIR
    })

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    print("=" * 60)
    print("Jarvis 3.0.1 Web Interface")
    print("=" * 60)
    print(f"Root directory: {ROOT_DIR}")
    print(f"Core modules available: {CORE_AVAILABLE}")
    print("Access the dashboard at: http://localhost:8080")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8080, debug=True)
