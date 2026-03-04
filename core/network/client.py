import requests
import json
import time
import threading

SYNC_URL = "http://localhost:5000"

def sync_memory(server_url=SYNC_URL):
    \"\"\"Синхронизация памяти с сервером\"\"\"
    try:
        print(f"[Client] Syncing with {server_url}")
        # Здесь будет логика синхронизации
        return True
    except Exception as e:
        print(f"[Client] Sync error: {e}")
        return False

def start_sync_loop(interval=60, server_url=SYNC_URL):
    \"\"\"Запускает цикл синхронизации\"\"\"
    def _loop():
        while True:
            sync_memory(server_url)
            time.sleep(interval)
    
    thread = threading.Thread(target=_loop, daemon=True)
    thread.start()
    print(f"[Client] Sync loop started (interval={interval}s)")
    return thread
