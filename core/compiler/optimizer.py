import hashlib
from collections import defaultdict

class GraphOptimizer:
    def init(self):
        self.patterns = []
    
    def optimize_graph(self, sqvgr):
        """Глобальная оптимизация графа действий"""
        sequence = sqvgr["sequence"]
        
        # Фаза 1: Удаление мёртвого кода (неиспользуемые init_counter)
        used_vars = set()
        for step in sequence:
            if step["action"] in ["increment", "loop_start"]:
                if step["action"] == "increment":
                    used_vars.add(step["target"])
                elif step["action"] == "loop_start":
                    var_name = step["condition"].split()[0]
                    used_vars.add(var_name)
        
        new_seq = []
        for step in sequence:
            if step["action"] == "init_counter" and step["target"] not in used_vars:
                print(f"[Compiler] Removing unused init_counter for {step['target']}")
                continue
            new_seq.append(step)
        
        # Фаза 2: Свёртка констант
        const_values = {}
        i = 0
        while i < len(new_seq):
            step = new_seq[i]
            if step["action"] == "init_counter":
                const_values[step["target"]] = step["value"]
            elif step["action"] == "increment" and step["target"] in const_values:
                const_values[step["target"]] += step["by"]
                # Можно заменить на новую инициализацию
                new_seq[i] = {
                    "step": step["step"],
                    "action": "init_counter",
                    "target": step["target"],
                    "value": const_values[step["target"]]
                }
            i += 1
        
        # Фаза 3: Оптимизация циклов с постоянным числом итераций
        i = 0
        while i < len(new_seq):
            if new_seq[i]["action"] == "loop_start":
                condition = new_seq[i]["condition"]
                var_name = condition.split()[0]
                limit = int(condition.split()[2])
                
                # Если переменная инициализирована константой и не меняется внутри
                if var_name in const_values:
                    init_val = const_values[var_name]
                    iterations = limit - init_val
                    if iterations <= 5 and iterations > 0:
                        print(f"[Compiler] Unrolling loop with {iterations} constant iterations")
                        # Находим тело цикла
                        loop_end_idx = i + 1
                        depth = 1
                        while loop_end_idx < len(new_seq):
                            if new_seq[loop_end_idx]["action"] == "loop_start":
                                depth += 1
                            elif new_seq[loop_end_idx]["action"] == "loop_end":
                                depth -= 1
                                if depth == 0:
                                    break
                            loop_end_idx += 1
                        
                        body = new_seq[i+1:loop_end_idx]
                        unrolled = []
                        for j in range(iterations):
                            for b in body:
                                if b["action"] != "increment":
                                    new_step = b.copy()
                                    new_step["step"] = i + len(unrolled) + 1
                                    unrolled.append(new_step)
                        new_seq = new_seq[:i] + unrolled + new_seq[loop_end_idx+1:]
                        # Перенумеруем
                        for idx, step in enumerate(new_seq):
                            step["step"] = idx + 1
                        break
            i += 1
        
        return {"sequence": new_seq}

_optimizer = GraphOptimizer()

def optimize_graph(sqvgr):
    return _optimizer.optimize_graph(sqvgr)