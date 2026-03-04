import time
import threading
import uuid
from collections import defaultdict
from core.network.discovery import get_nodes, start_discovery
from core.orchestrator.delegator import delegate_task, get_result, split_task
from core.life.scheduler import schedule_command

class DistributedOrchestrator:
    def init(self):
        self.node_tasks = defaultdict(list)
        self.task_history = []
        self.running = False
        self.monitor_thread = None
        self.node_id = str(uuid.uuid4())[:8]
    
    def start(self):
        """Запускает распределённый оркестратор"""
        if self.running:
            return
        
        self.running = True
        # Запускаем обнаружение узлов
        start_discovery()
        
        # Запускаем мониторинг
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        
        print(f"[Distributed] Orchestrator {self.node_id} started")
    
    def _monitor_loop(self):
        """Мониторит состояние узлов и перераспределяет задачи"""
        while self.running:
            nodes = get_nodes()
            print(f"[Distributed] Active nodes: {len(nodes)}")
            
            # Проверяем зависшие задачи
            now = time.time()
            for node_id, tasks in list(self.node_tasks.items()):
                if node_id not in nodes:
                    # Узел пропал, перераспределяем задачи
                    print(f"[Distributed] Node {node_id} lost, redistributing {len(tasks)} tasks")
                    for task in tasks:
                        self._redistribute_task(task)
                    del self.node_tasks[node_id]
            
            time.sleep(10)
    
    def _redistribute_task(self, task):
        """Перераспределяет задачу на другой узел"""
        result = delegate_task(task, sync=True)
        if result:
            print(f"[Distributed] Task redistributed, result: {result.get('status')}")
    
    def execute_distributed(self, command, split_strategy=None):
        """Выполняет команду в распределённом режиме"""
        print(f"[Distributed] Executing: {command}")
        
        nodes = get_nodes()
        if len(nodes) < 2:
            print("[Distributed] Not enough nodes, executing locally")
            from core.orchestrator.engine import run_orchestrator
            return run_orchestrator({"command": command})
        
        # Простейшее разделение - по словам
        if split_strategy == "words":
            words = command.split()
            if len(words) > 3:
                # Разбиваем на части
                mid = len(words) // 2
                cmd1 = " ".join(words[:mid])
                cmd2 = " ".join(words[mid:])
                
                subtasks = [
                    {"command": f"обработай {cmd1}"},
                    {"command": f"обработай {cmd2}"}
                ]
                
                results = split_task({"command": command}, subtasks)
                return {
                    "status": "distributed",
                    "results": results,
                    "nodes_used": len(nodes)
                }
        
        # По умолчанию - делегируем одному узлу
        task = {"command": command}
        result = delegate_task(task, sync=True)
        
        return {
            "status": "delegated",
            "result": result
        }
    
    def schedule_distributed(self, command, interval):
        """Планирует распределённое выполнение"""
        def _wrapper():
            return self.execute_distributed(command)
        
        schedule_command(f"distributed:{command}", interval)
        print(f"[Distributed] Scheduled: {command} every {interval}s")
    
    def stop(self):
        self.running = False
        print("[Distributed] Orchestrator stopped")

_distributed = DistributedOrchestrator()

def start_distributed():
    _distributed.start()
    return _distributed

def execute_distributed(command, split_strategy=None):
    return _distributed.execute_distributed(command, split_strategy)

def schedule_distributed(command, interval):
    return _distributed.schedule_distributed(command, interval)