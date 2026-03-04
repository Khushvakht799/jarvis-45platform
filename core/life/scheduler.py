import time
import threading
import heapq
from datetime import datetime, timedelta
from core.orchestrator.engine import run_orchestrator

class Scheduler:
    def init(self):
        self.tasks = []  # priority queue (timestamp, task_id, command)
        self.task_counter = 0
        self.lock = threading.Lock()
        self.running = False
        self.thread = None
    
    def add_task(self, command, run_at):
        """Добавляет задачу на конкретное время"""
        with self.lock:
            self.task_counter += 1
            task_id = f"task_{self.task_counter}"
            heapq.heappush(self.tasks, (run_at.timestamp(), task_id, command))
            print(f"[Scheduler] Task {task_id} scheduled at {run_at}")
            return task_id
    
    def add_recurring(self, command, interval_seconds):
        """Добавляет повторяющуюся задачу"""
        run_at = datetime.now() + timedelta(seconds=interval_seconds)
        task_id = self.add_task(command, run_at)
        # Сохраняем интервал для повторения
        with self.lock:
            if not hasattr(self, 'recurring'):
                self.recurring = {}
            self.recurring[task_id] = (command, interval_seconds)
        return task_id
    
    def start(self):
        """Запускает планировщик в фоновом потоке"""
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()
        print("[Scheduler] Started")
    
    def _run_loop(self):
        while self.running:
            now = datetime.now()
            with self.lock:
                while self.tasks and self.tasks[0][0] <= now.timestamp():
                    ts, task_id, command = heapq.heappop(self.tasks)
                    print(f"[Scheduler] Executing task {task_id}: {command}")
                    # Запускаем команду
                    threading.Thread(target=self._execute_task, args=(command,)).start()
                    
                    # Если задача повторяющаяся, перепланируем
                    if hasattr(self, 'recurring') and task_id in self.recurring:
                        cmd, interval = self.recurring[task_id]
                        new_time = datetime.fromtimestamp(ts) + timedelta(seconds=interval)
                        heapq.heappush(self.tasks, (new_time.timestamp(), task_id, cmd))
                        print(f"[Scheduler] Rescheduled {task_id} at {new_time}")
            time.sleep(1)
    
    def _execute_task(self, command):
        """Выполняет задачу в отдельном потоке"""
        try:
            input_json = {"command": command}
            result = run_orchestrator(input_json, sync=False)
            print(f"[Scheduler] Task result: {result.get('status')}")
        except Exception as e:
            print(f"[Scheduler] Task error: {e}")
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        print("[Scheduler] Stopped")

# Глобальный экземпляр
_scheduler = Scheduler()

def start_scheduler():
    _scheduler.start()
    return _scheduler

def schedule_command(command, run_at):
    return _scheduler.add_task(command, run_at)

def schedule_recurring(command, interval_seconds):
    return _scheduler.add_recurring(command, interval_seconds)