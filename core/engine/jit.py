import time
from collections import defaultdict

class JITCompiler:
    def init(self):
        self.execution_stats = defaultdict(lambda: {"count": 0, "total_time": 0, "last_optimized": None})
        self.optimized_versions = {}
    
    def record_execution(self, sequence_id, step_index, execution_time):
        key = f"{sequence_id}:{step_index}"
        self.execution_stats[key]["count"] += 1
        self.execution_stats[key]["total_time"] += execution_time
    
    def should_optimize(self, sequence_id, step_index, threshold_count=5, threshold_time=0.01):
        key = f"{sequence_id}:{step_index}"
        stats = self.execution_stats.get(key, {"count": 0, "total_time": 0})
        avg_time = stats["total_time"] / max(stats["count"], 1)
        return stats["count"] >= threshold_count and avg_time > threshold_time
    
    def optimize_step(self, sequence, step_index, state):
        step = sequence[step_index]
        action = step["action"]
        
        print(f"[JIT] Optimizing step {step_index+1}: {action}")
        
        if action == "loop_start":
            loop_end_idx = step_index + 1
            depth = 1
            while loop_end_idx < len(sequence):
                if sequence[loop_end_idx]["action"] == "loop_start":
                    depth += 1
                elif sequence[loop_end_idx]["action"] == "loop_end":
                    depth -= 1
                    if depth == 0:
                        break
                loop_end_idx += 1
            
            body_length = loop_end_idx - step_index - 1
            condition = step["condition"]
            var_name = condition.split()[0]
            limit = int(condition.split()[2])
            
            if body_length <= 3 and limit <= 10:
                print(f"[JIT] Unrolling loop with {limit} iterations")
                body = sequence[step_index+1:loop_end_idx]
                unrolled = []
                for i in range(limit):
                    for b in body:
                        if b["action"] != "increment":
                            new_step = b.copy()
                            new_step["step"] = step_index + len(unrolled) + 1
                            unrolled.append(new_step)
                new_sequence = sequence[:step_index] + unrolled + sequence[loop_end_idx+1:]
                return new_sequence
        
        return sequence

_jit = JITCompiler()

def record_execution(sequence_id, step_index, execution_time):
    _jit.record_execution(sequence_id, step_index, execution_time)

def should_optimize(sequence_id, step_index):
    return _jit.should_optimize(sequence_id, step_index)

def optimize_step(sequence, step_index, state):
    return _jit.optimize_step(sequence, step_index, state)