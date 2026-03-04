import datetime
import os
import json
import random

def get_time():
    """Возвращает текущее время"""
    now = datetime.datetime.now()
    return {
        "timestamp": now.isoformat(),
        "hour": now.hour,
        "minute": now.minute,
        "second": now.second,
        "day": now.day,
        "month": now.month,
        "year": now.year,
        "weekday": now.weekday()
    }

def read_file(path):
    """Читает содержимое файла"""
    try:
        with open(path, 'r') as f:
            content = f.read()
        return {"status": "ok", "content": content, "path": path}
    except Exception as e:
        return {"status": "error", "error": str(e), "path": path}

def file_exists(path):
    """Проверяет существование файла"""
    return {"exists": os.path.exists(path), "path": path}

def list_dir(path="."):
    """Список файлов в директории"""
    try:
        files = os.listdir(path)
        return {"status": "ok", "files": files, "path": path}
    except Exception as e:
        return {"status": "error", "error": str(e), "path": path}

def get_env(key):
    """Получает переменную окружения"""
    value = os.environ.get(key)
    return {"key": key, "value": value, "exists": value is not None}

def random_number(min_val=0, max_val=100):
    """Генерирует случайное число"""
    return {"value": random.randint(min_val, max_val), "min": min_val, "max": max_val}