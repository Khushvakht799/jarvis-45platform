import random
from datetime import datetime, timedelta
from core.metacontrol.memory import load_memory
from core.metacontrol.vectorizer import cosine_similarity, text_to_vector
from core.life.scheduler import schedule_command

class GoalGenerator:
    def init(self):
        self.goal_templates = [
            {"command": "сколько времени", "reason": "learn time patterns"},
            {"command": "случайное число", "reason": "practice randomness"},
            {"command": "скажи привет три раза", "reason": "reinforce output"}
        ]
    
    def analyze_memory(self):
        """Анализирует память и генерирует цели"""
        memory = load_memory()
        goals = []
        
        # Если мало опыта, добавляем базовые цели
        if len(memory["experiences"]) < 5:
            goals.append({
                "command": "сколько времени",
                "priority": 1,
                "reason": "initial exploration"
            })
        
        # Если есть неизвестные команды
        unknown_count = sum(1 for e in memory["experiences"] 
                          if e["avgr"]["intent"]["type"] == "unknown")
        if unknown_count > 3:
            goals.append({
                "command": "помощь",
                "priority": 2,
                "reason": "many unknown commands"
            })
        
        # Если есть успешные паттерны, пробуем вариации
        if "patterns" in memory and memory["patterns"]:
            # Берём случайный паттерн и создаём похожую команду
            pattern_key = random.choice(list(memory["patterns"].keys()))
            if pattern_key.startswith("execute_command_output"):
                goals.append({
                    "command": "скажи привет два раза",
                    "priority": 3,
                    "reason": f"explore variation of {pattern_key}"
                })
        
        return goals
    
    def generate_goals(self, max_goals=3):
        """Генерирует список целей для автономного выполнения"""
        goals = self.analyze_memory()
        
        # Добавляем случайные шаблоны для разнообразия
        while len(goals) < max_goals:
            template = random.choice(self.goal_templates)
            if not any(g["command"] == template["command"] for g in goals):
                goals.append({
                    "command": template["command"],
                    "priority": random.randint(1, 5),
                    "reason": template["reason"]
                })
        
        # Сортируем по приоритету
        goals.sort(key=lambda x: x["priority"])
        return goals[:max_goals]

_goal_generator = GoalGenerator()

def generate_goals():
    return _goal_generator.generate_goals()