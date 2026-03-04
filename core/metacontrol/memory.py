import json
import os
from datetime import datetime
from collections import defaultdict
from core.metacontrol.vectorizer import text_to_vector, avgr_to_vector, sqvgr_to_vector, cosine_similarity

MEMORY_FILE = "jarvis_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {"experiences": [], "best_sequences": {}, "patterns": {}, "vectors": []}

def save_memory(memory):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)

def add_experience(command, avgr, sqvgr, bvgr, givgr, syvgr):
    memory = load_memory()
    
    cmd_vec = text_to_vector(command)
    avgr_vec = avgr_to_vector(avgr)
    sqvgr_vec = sqvgr_to_vector(sqvgr)
    
    exp = {
        "timestamp": datetime.now().isoformat(),
        "command": command,
        "command_vector": cmd_vec,
        "avgr": avgr,
        "avgr_vector": avgr_vec,
        "sqvgr": sqvgr,
        "sqvgr_vector": sqvgr_vec,
        "bvgr": bvgr,
        "givgr": givgr,
        "syvgr": syvgr
    }
    memory["experiences"].append(exp)
    memory["vectors"].append({
        "command": command,
        "cmd_vec": cmd_vec,
        "avgr_vec": avgr_vec,
        "sqvgr_vec": sqvgr_vec,
        "index": len(memory["experiences"]) - 1
    })
    
    if syvgr["symptom"]["status"] == "success":
        key = command[:50]
        if key not in memory["best_sequences"] or syvgr["symptom"].get("deviation", 999) < memory["best_sequences"].get(key, {}).get("deviation", 999):
            memory["best_sequences"][key] = {
                "sqvgr": sqvgr,
                "deviation": syvgr["symptom"].get("deviation", 0),
                "length": len(sqvgr["sequence"]),
                "timestamp": datetime.now().isoformat(),
                "vector": sqvgr_vec
            }
        
        pattern_key = f"{avgr['intent']['type']}{avgr['intent']['command']}"
        if pattern_key not in memory["patterns"]:
            memory["patterns"][pattern_key] = {"count": 0, "avg_length": 0, "sequences": []}
        
        p = memory["patterns"][pattern_key]
        p["count"] += 1
        p["avg_length"] = (p["avg_length"] * (p["count"] - 1) + len(sqvgr["sequence"])) / p["count"]
        p["sequences"].append({
            "length": len(sqvgr["sequence"]),
            "deviation": syvgr["symptom"].get("deviation", 0),
            "timestamp": datetime.now().isoformat()
        })
    
    save_memory(memory)
    return memory

def find_similar_by_vector(vector, threshold=0.7, limit=5):
    memory = load_memory()
    similarities = []
    for idx, v in enumerate(memory.get("vectors", [])):
        sim = cosine_similarity(vector, v["cmd_vec"])
        if sim > threshold:
            similarities.append((sim, idx, v))
    similarities.sort(reverse=True)
    result = []
    for sim, idx, v in similarities[:limit]:
        result.append(memory["experiences"][v["index"]])
    return result

def find_similar_commands(command, limit=5):
    cmd_vec = text_to_vector(command)
    similar = find_similar_by_vector(cmd_vec, threshold=0.5, limit=limit)
    if similar:
        return similar
    memory = load_memory()
    matches = [exp for exp in memory["experiences"] if command in exp["command"] or exp["command"] in command]
    return matches[-limit:]

def get_best_sequence(command):
    memory = load_memory()
    key = command[:50]
    if key in memory["best_sequences"]:
        return memory["best_sequences"][key]["sqvgr"]
    
    cmd_vec = text_to_vector(command)
    best_sim = 0
    best_sqvgr = None
    for seq_key, seq_data in memory["best_sequences"].items():
        if "vector" in seq_data:
            sim = cosine_similarity(cmd_vec, seq_data["vector"])
            if sim > best_sim and sim > 0.6:
                best_sim = sim
                best_sqvgr = seq_data["sqvgr"]
    return best_sqvgr

def get_pattern_stats(intent_type, intent_command):
    memory = load_memory()
    pattern_key = f"{intent_type}{intent_command}"
    return memory["patterns"].get(pattern_key, {})