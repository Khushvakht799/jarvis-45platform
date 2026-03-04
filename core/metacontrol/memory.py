import json
import os
from datetime import datetime

MEMORY_FILE = "jarvis_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {"experiences": [], "best_sequences": {}, "patterns": {}}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2)

def add_experience(command, avgr, sqvgr, bvgr, givgr, syvgr):
    memory = load_memory()
    memory["experiences"].append({
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "avgr": avgr,
        "sqvgr": sqvgr,
        "bvgr": bvgr,
        "givgr": givgr,
        "syvgr": syvgr
    })
    save_memory(memory)
    return memory
