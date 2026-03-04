import hashlib
import json
import os
import time
from collections import OrderedDict

class CompilerCache:
    def init(self, cache_file="compiler_cache.json", max_size=100):
        self.cache_file = cache_file
        self.max_size = max_size
        self.cache = self._load_cache()
    
    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
            except:
                return {"entries": OrderedDict(), "stats": {"hits": 0, "misses": 0}}
        return {"entries": OrderedDict(), "stats": {"hits": 0, "misses": 0}}
    
    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def _hash_key(self, avgr, context=None):
        """Генерирует ключ кэша на основе AVGr и контекста"""
        key_data = json.dumps(avgr, sort_keys=True)
        if context:
            key_data += json.dumps(context, sort_keys=True)
        return hashlib.sha256(key_data.encode()).hexdigest()[:16]
    
    def get(self, avgr, context=None):
        """Получает скомпилированную последовательность из кэша"""
        key = self._hash_key(avgr, context)
        if key in self.cache["entries"]:
            entry = self.cache["entries"][key]
            # Обновляем время последнего доступа
            entry["last_access"] = time.time()
            self.cache["stats"]["hits"] += 1
            self._save_cache()
            print(f"[Cache] Hit for {key}")
            return entry["result"]
        
        self.cache["stats"]["misses"] += 1
        self._save_cache()
        print(f"[Cache] Miss for {key}")
        return None
    
    def put(self, avgr, result, context=None, metadata=None):
        """Сохраняет результат компиляции в кэш"""
        key = self._hash_key(avgr, context)
        
        # Проверяем размер кэша
        if len(self.cache["entries"]) >= self.max_size:
            # Удаляем самую старую запись
            oldest_key = min(self.cache["entries"].keys(), 
                           key=lambda k: self.cache["entries"][k]["last_access"])
            del self.cache["entries"][oldest_key]
            print(f"[Cache] Removed oldest entry: {oldest_key}")
        
        self.cache["entries"][key] = {
            "timestamp": time.time(),
            "last_access": time.time(),
            "avgr": avgr,
            "result": result,
            "metadata": metadata or {}
        }
        self._save_cache()
        print(f"[Cache] Stored {key}")
    
    def invalidate(self, avgr_pattern=None):
        """Инвалидирует записи по шаблону"""
        if avgr_pattern is None:
            self.cache["entries"] = OrderedDict()
            print("[Cache] Cleared")
        else:
            # Удаляем по шаблону (упрощённо)
            keys_to_delete = []
            for key, entry in self.cache["entries"].items():
                if entry["avgr"].get("intent", {}).get("type") == avgr_pattern:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                del self.cache["entries"][key]
            print(f"[Cache] Invalidated {len(keys_to_delete)} entries")
        self._save_cache()
    
    def get_stats(self):
        """Возвращает статистику кэша"""
        stats = self.cache["stats"].copy()
        stats["size"] = len(self.cache["entries"])
        stats["hit_rate"] = stats["hits"] / (stats["hits"] + stats["misses"]) if (stats["hits"] + stats["misses"]) > 0 else 0
        return stats

_cache = CompilerCache()

def cache_get(avgr, context=None):
    return _cache.get(avgr, context)

def cache_put(avgr, result, context=None, metadata=None):
    _cache.put(avgr, result, context, metadata)

def cache_invalidate(pattern=None):
    _cache.invalidate(pattern)

def cache_stats():
    return _cache.get_stats()