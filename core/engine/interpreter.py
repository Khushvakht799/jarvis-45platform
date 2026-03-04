from core.framework.output import console_output

def execute_sequence(sequence, state, sequence_id="default", start=0, end=None):
    \"\"\"Минимальный интерпретатор\"\"\"
    if end is None:
        end = len(sequence)
    
    idx = start
    while idx < end:
        step = sequence[idx]
        action = step["action"]
        
        if action == "console_output":
            console_output(step["value"])
            if "output_log" not in state:
                state["output_log"] = []
            state["output_log"].append(step["value"])
            idx += 1
        elif action == "return":
            return {"status": step["value"], "final_state": state}
        else:
            idx += 1
    
    return {"status": "completed", "final_state": state}
