class CompilerCache:
    def __init__(self):
        self.hits = 0
        self.misses = 0
        self.cache = {}
    
    def get_stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "size": len(self.cache),
            "hit_rate": hit_rate
        }

_cache = CompilerCache()

def cache_stats():
    return _cache.get_stats()
