import hashlib
import math

class Vectorizer:
    def init(self):
        self.dim = 128
    
    def hash_token(self, token, seed=0):
        h = hashlib.md5(f"{token}{seed}".encode()).hexdigest()
        return int(h, 16) % self.dim
    
    def text_to_vector(self, text):
        words = text.lower().split()
        vec = [0] * self.dim
        for word in words:
            idx = self._hash_token(word)
            vec[idx] += 1
        norm = math.sqrt(sum(xx for x in vec))
        if norm > 0:
            vec = [x/norm for x in vec]
        return vec
    
    def avgr_to_vector(self, avgr):
        vec = [0] * self.dim
        if "intent" in avgr:
            intent = avgr["intent"]
            idx = self._hash_token(intent.get("type", "unknown"), seed=1)
            vec[idx] += 1
            idx = self._hash_token(intent.get("command", "unknown"), seed=2)
            vec[idx] += 1
            for k, v in intent.get("params", {}).items():
                idx = self.hash_token(f"{k}{v}", seed=3)
                vec[idx] += 1
            if "repeat" in intent:
                idx = self.hash_token(f"repeat{intent['repeat']}", seed=4)
                vec[idx] += 1
        norm = math.sqrt(sum(xx for x in vec))
        if norm > 0:
            vec = [x/norm for x in vec]
        return vec
    
    def sqvgr_to_vector(self, sqvgr):
        vec = [0] * self.dim
        for step in sqvgr.get("sequence", []):
            action = step.get("action", "")
            idx = self.hash_token(f"action{action}", seed=5)
            vec[idx] += 1
        norm = math.sqrt(sum(xx for x in vec))
        if norm > 0:
            vec = [x/norm for x in vec]
        return vec
    
    def cosine_similarity(self, v1, v2):
        dot = sum(ab for a,b in zip(v1, v2))
        return dot

_vectorizer = Vectorizer()

def text_to_vector(text):
    return _vectorizer.text_to_vector(text)

def avgr_to_vector(avgr):
    return _vectorizer.avgr_to_vector(avgr)

def sqvgr_to_vector(sqvgr):
    return vectorizer.sqvgr_to_vector(sqvgr)

def cosine_similarity(v1, v2):
    return vectorizer.cosine_similarity(v1, v2)