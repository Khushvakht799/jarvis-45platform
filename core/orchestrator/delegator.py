import json
import hashlib
import requests
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from core.network.discovery import get_nodes

class TaskDelegator:
    def init(self):
        self.executor = ThreadPoolExecutor(max_workers=10)
        self.pending_tasks = {}
        self.results = {}
        self.result_ready = threading.Event()
    
    def delegate_task(self, task, node=None, sync=True):
        """Делегирует задачу узлу"""
        task_id = hashlib.md5(json.dumps(task, sort_keys=True).encode() + str(time.time()).encode()).hexdigest()[:8]
        
        if node is None:
            # Выбираем узел с наименьшей нагрузкой
            nodes = get_nodes()
            if not nodes:
                print("[Delegator] No nodes available")
                return None
            # Простейший выбор - первый попавшийся
            node = list(nodes.values())[0]
        
        print(f"[Delegator] Delegating task {task_id} to {node['address']}")
        
        # Создаём запись о задаче
        self.pending_tasks[task_id] = {
            "node": node,
            "task": task,
            "start_time": time.time(),
            "status": "pending"
        }
        
        if sync:
            # Синхронное выполнение - ждём результат
            result = self._execute_remote(node, task, task_id)
            self.results[task_id] = result
            return result
        else:
            # Асинхронное - возвращаем task_id
            future = self.executor.submit(self._execute_remote, node, task, task_id)
            self.pending_tasks[task_id]["future"] = future
            return task_id
    
    def _execute_remote(self, node, task, task_id):
        """Выполняет задачу на удалённом узле"""
        try:
            url = f"http://{node['address']}:5001/execute"
            response = requests.post(url, json=task, timeout=30)
            if response.status_code == 200:
                result = response.json()
                # Если результат асинхронный, может вернуть task_id
                if result.get("status") == "accepted" and "task_id" in result:
                    # Опрашиваем результат
                    remote_task_id = result["task_id"]
                    return self._poll_result(node, remote_task_id, task_id)
                else:
                    self.results[task_id] = result
                    self.pending_tasks[task_id]["status"] = "completed"
                    return result
            else:
                print(f"[Delegator] Remote error: {response.status_code}")
                result = {"error": f"HTTP {response.status_code}"}
                self.results[task_id] = result
                self.pending_tasks[task_id]["status"] = "error"
                return result
        except Exception as e:
            print(f"[Delegator] Remote execution error: {e}")
            result = {"error": str(e)}
            self.results[task_id] = result
            self.pending_tasks[task_id]["status"] = "error"
            return result
    
    def _poll_result(self, node, remote_task_id, local_task_id, max_attempts=30):
        """Опрашивает удалённый узел для получения результата"""
        for attempt in range(max_attempts):
            try:
                url = f"http://{node['address']}:5001/result/{remote_task_id}"
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    result = response.json()
                    if result.get("status") == "completed":
                        self.results[local_task_id] = result
                        self.pending_tasks[local_task_id]["status"] = "completed"
                        return result
                    elif result.get("status") == "pending":
                        time.sleep(1)
                        continue
                else:
                    time.sleep(1)
            except:
                time.sleep(1)
        
        result = {"error": "Timeout waiting for result"}
        self.results[local_task_id] = result
        self.pending_tasks[local_task_id]["status"] = "timeout"
        return result
    
    def get_result(self, task_id, timeout=None):
        """Получает результат задачи"""
        if task_id in self.results:
            return self.results[task_id]
        
        if task_id in self.pending_tasks:
            future = self.pending_tasks[task_id].get("future")
            if future:
                try:
                    result = future.result(timeout=timeout)
                    return result
                except Exception as e:
                    return {"error": str(e)}
        
        return {"error": "Task not found"}
    
    def split_task(self, task, subtasks):
        """Разбивает задачу на подзадачи"""
        results = []
        task_ids = []
        
        for subtask in subtasks:
            task_id = self.delegate_task(subtask, sync=False)
            if task_id:
                task_ids.append(task_id)
        
        # Собираем результаты
        for task_id in task_ids:
            result = self.get_result(task_id, timeout=30)
            results.append(result)
        
        return results

_delegator = TaskDelegator()

def delegate_task(task, node=None, sync=True):
    return _delegator.delegate_task(task, node, sync)

def get_result(task_id, timeout=None):
    return _delegator.get_result(task_id, timeout)

def split_task(task, subtasks):
    return _delegator.split_task(task, subtasks)