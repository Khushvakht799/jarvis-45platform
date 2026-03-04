import os
import json
from datetime import datetime

def write_file(path, content, mode="w"):
    """Записывает данные в файл"""
    try:
        with open(path, mode) as f:
            f.write(content)
        return {"status": "ok", "path": path, "mode": mode, "size": len(content)}
    except Exception as e:
        return {"status": "error", "error": str(e), "path": path}

def append_file(path, content):
    """Добавляет данные в конец файла"""
    return write_file(path, content, "a")

def log_event(event_type, data, logfile="jarvis.log"):
    """Записывает событие в лог-файл"""
    try:
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {event_type}: {json.dumps(data, ensure_ascii=False)}
"
        with open(logfile, "a") as f:
            f.write(log_entry)
        return {"status": "ok", "logfile": logfile}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def notify(message, level="info"):
    """Отправляет уведомление (пока просто в консоль)"""
    print(f"[NOTIFICATION][{level.upper()}]: {message}")
    return {"status": "ok", "message": message, "level": level}

def delete_file(path):
    """Удаляет файл"""
    try:
        os.remove(path)
        return {"status": "ok", "path": path}
    except Exception as e:
        return {"status": "error", "error": str(e), "path": path}

def create_directory(path):
    """Создаёт директорию"""
    try:
        os.makedirs(path, exist_ok=True)
        return {"status": "ok", "path": path}
    except Exception as e:
        return {"status": "error", "error": str(e), "path": path}