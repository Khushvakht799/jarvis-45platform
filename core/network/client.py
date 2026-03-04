import requests
import json
import time
from core.metacontrol.memory import load_memory, save_memory

SYNC_URL = "http://localhost:5000"

def sync_memory(server_url=SYNC_URL):
    try:
        local = load_memory()
        
        response = requests.post(
            f"{server_url}/sync",
            json={
                "experiences": local["experiences"][-10:],
                "best_sequences": local["best_sequences"],
                "patterns": local["patterns"]
            },
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"[Network] Synced with server, got {len(data.get('experiences', []))} new experiences")
            
            if "experiences" in data:
                existing_timestamps = {e["timestamp"] for e in local["experiences"]}
                for exp in data["experiences"]:
                    if exp["timestamp"] not in existing_timestamps:
                        local["experiences"].append(exp)
            
            if "best_sequences" in data:
                for key, val in data["best_sequences"].items():
                    if key not in local["best_sequences"] or val["deviation"] < local["best_sequences"][key]["deviation"]:
                        local["best_sequences"][key] = val
            
            if "patterns" in data:
                for key, val in data["patterns"].items():
                    if key not in local["patterns"]:
                        local["patterns"][key] = val
                    else:
                        p = local["patterns"][key]
                        p["count"] += val["count"]
                        p["avg_length"] = (p["avg_length"] * (p["count"] - val["count"]) + val["avg_length"] * val["count"]) / p["count"]
                        p["sequences"].extend(val["sequences"])
            
            save_memory(local)
            return True
    except Exception as e:
        print(f"[Network] Sync error: {e}")
    return False

def start_sync_loop(interval=60, server_url=SYNC_URL):
    import threading
    
    def _loop():
        while True:
            sync_memory(server_url)
            time.sleep(interval)
    
    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
    print(f"[Network] Sync loop started (interval={interval}s)")
    return thread