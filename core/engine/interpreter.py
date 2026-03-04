from core.framework.output import console_output

def execute_sequence(sequence, state, start=0, end=None):
    if end is None:
        end = len(sequence)
    
    idx = start
    while idx < end:
        step = sequence[idx]
        action = step["action"]
        
        if action == "init_counter":
            state[step["target"]] = step["value"]
            idx += 1
        
        elif action == "console_output":
            console_output(step["value"])
            if "output_log" not in state:
                state["output_log"] = []
            state["output_log"].append(step["value"])
            idx += 1
        
        elif action == "increment":
            state[step["target"]] += step["by"]
            idx += 1
        
        elif action == "loop_start":
            condition = step["condition"]
            var_name = condition.split()[0]
            limit = int(condition.split()[2])
            
            loop_end_idx = idx + 1
            depth = 1
            while loop_end_idx < len(sequence):
                if sequence[loop_end_idx]["action"] == "loop_start":
                    depth += 1
                elif sequence[loop_end_idx]["action"] == "loop_end":
                    depth -= 1
                    if depth == 0:
                        break
                loop_end_idx += 1
            
            while state.get(var_name, 0) < limit:
                execute_sequence(sequence, state, idx + 1, loop_end_idx)
            
            idx = loop_end_idx + 1
        
        elif action == "loop_end":
            return
        
        elif action == "return":
            return {"status": step["value"], "final_state": state}
        
        else:
            idx += 1
    
    return {"status": "completed", "final_state": state}

if __name__ == "__main__":
    test_sq = {
        "sequence": [
            {"step": 1, "action": "init_counter", "target": "count", "value": 0},
            {"step": 2, "action": "loop_start", "condition": "count < 3"},
            {"step": 3, "action": "console_output", "value": "привет"},
            {"step": 4, "action": "increment", "target": "count", "by": 1},
            {"step": 5, "action": "loop_end"},
            {"step": 6, "action": "return", "value": "success"}
        ]
    }
    test_state = {"count": 0, "output_log": []}
    result = execute_sequence(test_sq["sequence"], test_state)
    print("Test result:", result)
