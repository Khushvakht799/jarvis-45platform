import time
import threading
import random
from datetime import datetime, timedelta
from core.life.scheduler import schedule_command, schedule_recurring, start_scheduler
from core.life.goals import generate_goals
from core.metacontrol.memory import load_memory
from core.orchestrator.engine import run_orchestrator

class AutonomyEngine:
    def init(self):
        self.running = False
        self.thread = None
        self.learning_interval = 3600  # 1 час
        self.last_learning = datetime.now()
    
    def start(self):
        """Запускает автономный режим"""
        if self.running:
            return
        
        self.running = True
        # Запускаем планировщик
        start_scheduler()
        
        # Планируем регулярное самообучение
        schedule_recurring("learn", self.learning_interval)
        
        # Планируем случайные исследовательские задачи
        self._schedule_exploration()
        
        # Запускаем фоновый поток для мониторинга
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        print("[Autonomy] Engine started")
    
    def _schedule_exploration(self):
        """Планирует случайные исследовательские задачи"""
        # Каждые 15-30 минут выполнять случайную цель
        goals = generate_goals()
        for goal in goals:
            delay = random.randint(900, 1800)  # 15-30 минут
            run_at = datetime.now() + timedelta(seconds=delay)
            schedule_command(goal["command"], run_at)
            print(f"[Autonomy] Scheduled exploration: {goal['command']} at {run_at}")
    
    def _monitor_loop(self):
        """Фоновый мониторинг состояния"""
        while self.running:
            time.sleep(60)  # проверка каждую минуту
            
            # Проверяем, не пора ли перепланировать
            if datetime.now() - self.last_learning > timedelta(hours=6):
                self.last_learning = datetime.now()
                self._schedule_exploration()
                
                # Анализируем прогресс
                memory = load_memory()
                success_rate = self._calculate_success_rate(memory)
                print(f"[Autonomy] Success rate: {success_rate:.2f}%")
    
    def _calculate_success_rate(self, memory):
        """Вычисляет процент успешных выполнений"""
        experiences = memory.get("experiences", [])
        if not experiences:
            return 0
        success = sum(1 for e in experiences 
                     if e["syvgr"]["symptom"]["status"] == "success")
        return (success / len(experiences)) * 100
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[Autonomy] Engine stopped")

# Глобальный экземпляр
_autonomy = AutonomyEngine()

def start_autonomy():
    _autonomy.start()
    return _autonomy

def process_learning_command(command):
    """Обрабатывает внутренние команды обучения"""
    if command == "learn":
        print("[Autonomy] Learning cycle triggered")
        goals = generate_goals()
        for goal in goals:
            print(f"[Autonomy] Learning goal: {goal['command']} ({goal['reason']})")
            # Можно выполнять прямо сейчас или планировать
        return {"status": "learning", "goals": goals}
    return None