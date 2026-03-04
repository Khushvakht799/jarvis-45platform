from flask import Flask, request, jsonify
import json
import os
import threading
import uuid
import time
from datetime import datetime
from core.orchestrator.engine import run_orchestrator

app = Flask(name)

SERVER_MEMORY_FILE = "server_memory.json"

# Хранилище для асинхронных задач
async_tasks = {}

def load_server_memory():
    if os.path.exists(SERVER_MEMORY_FILE):
        with open(SERVER_MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {"experiences": [], "best_sequences": {}, "patterns": {}, "nodes": []}

def save_server_memory(memory):
    with open(SERVER_MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

@app.route('/sync', methods=['POST'])
def sync():
    data = request.json
    memory = load_server_memory()
    
    client_id = request.remote_addr
    timestamp = datetime.now().isoformat()
    
    if client_id not in [n["id"] for n in memory["nodes"]]:
        memory["nodes"].append({
            "id": client_id,
            "first_seen": timestamp,
            "last_seen": timestamp,
            "type": "sync"
        })
    else:
        for n in memory["nodes"]:
            if n["id"] == client_id:
                n["last_seen"] = timestamp
    
    if "experiences" in data:
        existing_timestamps = {e["timestamp"] for e in memory["experiences"]}
        for exp in data["experiences"]:
            if exp["timestamp"] not in existing_timestamps:
                exp["source"] = client_id
                memory["experiences"].append(exp)
    
    if "best_sequences" in data:
        for key, val in data["best_sequences"].items():
            if key not in memory["best_sequences"] or val["deviation"] < memory["best_sequences"][key]["deviation"]:
                val["source"] = client_id
                memory["best_sequences"][key] = val
    
    if "patterns" in data:
        for key, val in data["patterns"].items():
            if key not in memory["patterns"]:
                memory["patterns"][key] = val
            else:
                p = memory["patterns"][key]
                p["count"] += val["count"]
                p["avg_length"] = (p["avg_length"] * (p["count"] - val["count"]) + val["avg_length"] * val["count"]) / p["count"]
                p["sequences"].extend(val["sequences"])
    
    save_server_memory(memory)
    
    return jsonify({
        "experiences": memory["experiences"][-50:],
        "best_sequences": memory["best_sequences"],
        "patterns": memory["patterns"]
    })

@app.route('/execute', methods=['POST'])
def execute():
    """Endpoint для удалённого выполнения команд (асинхронный)"""
    data = request.json
    print(f"[Remote] Received task: {data}")
    
    # Генерируем ID задачи
    task_id = str(uuid.uuid4())[:8]
    
    # Создаём запись о задаче
    async_tasks[task_id] = {
        "status": "pending",
        "created": time.time(),
        "data": data,
        "result": None
    }
    
    # Запускаем выполнение в отдельном потоке
    def _run():
        result = run_orchestrator(data, sync=False)
        async_tasks[task_id]["status"] = "completed"
        async_tasks[task_id]["result"] = result
        print(f"[Remote] Task {task_id} completed")
    
    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    
    return jsonify({
        "status": "accepted",
        "task_id": task_id,
        "message": "Task accepted for execution"
    })

@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    """Получение результата асинхронной задачи"""
    if task_id not in async_tasks:
        return jsonify({"error": "Task not found"}), 404
    
    task = async_tasks[task_id]
    if task["status"] == "completed":
        return jsonify({
            "status": "completed",
            "result": task["result"]
        })
    else:
        return jsonify({
            "status": "pending",
            "created": task["created"]
        })

@app.route('/nodes', methods=['GET'])
def nodes():
    """Возвращает список активных узлов"""
    memory = load_server_memory()
    return jsonify({
        "nodes": memory["nodes"],
        "count": len(memory["nodes"])
    })

@app.route('/stats', methods=['GET'])
def stats():
    memory = load_server_memory()
    return jsonify({
        "nodes": len(memory["nodes"]),
        "experiences": len(memory["experiences"]),
        "best_sequences": len(memory["best_sequences"]),
        "patterns": len(memory["patterns"])
    })

if name == 'main':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)