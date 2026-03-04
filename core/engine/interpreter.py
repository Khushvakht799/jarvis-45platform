import time
from core.framework.output import console_output
from core.engine.jit import record_execution, should_optimize, optimize_step
from core.physics.sensors import get_time, read_file, file_exists, list_dir, get_env, random_number
from core.physics.actuators import write_file, append_file, log_event, notify, delete_file, create_directory

def execute_sequence(sequence, state, sequence_id="default", start=0, end=None):
    if end is None:
        end = len(sequence)
    
    idx = start
    while idx < end:
        step = sequence[idx]
        action = step["action"]
        
        if should_optimize(sequence_id, idx):
            new_sequence = optimize_step(sequence, idx, state)
            if new_sequence != sequence:
                print(f"[JIT] Step {idx+1} optimized, restarting execution")
                return execute_sequence(new_sequence, state, sequence_id, start, end)
        
        start_time = time.time()
        
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
                execute_sequence(sequence, state, sequence_id, idx + 1, loop_end_idx)
            
            idx = loop_end_idx + 1
        
        elif action == "loop_end":
            return
        
        elif action == "return":
            return {"status": step["value"], "final_state": state}
        
        elif action == "get_time":
            result = get_time()
            state["last_sensor_result"] = result
            if "sensor_log" not in state:
                state["sensor_log"] = []
            state["sensor_log"].append({"action": "get_time", "result": result})
            idx += 1
        
        elif action == "read_file":
            path = step.get("path", "")
            result = read_file(path)
            state["last_sensor_result"] = result
            state["sensor_log"] = state.get("sensor_log", []) + [{"action": "read_file", "result": result}]
            if result["status"] == "ok":
                state["file_content"] = result["content"]
            idx += 1
        
        elif action == "file_exists":
            path = step.get("path", "")
            result = file_exists(path)
            state["last_sensor_result"] = result
            state["sensor_log"] = state.get("sensor_log", []) + [{"action": "file_exists", "result": result}]
            idx += 1
        
        elif action == "list_dir":
            path = step.get("path", ".")
            result = list_dir(path)
            state["last_sensor_result"] = result
            state["sensor_log"] = state.get("sensor_log", []) + [{"action": "list_dir", "result": result}]
            idx += 1
        
        elif action == "random_number":
            min_val = step.get("min", 0)
            max_val = step.get("max", 100)
            result = random_number(min_val, max_val)
            state["last_sensor_result"] = result
            state["sensor_log"] = state.get("sensor_log", []) + [{"action": "random_number", "result": result}]
            idx += 1
        
        elif action == "write_file":
            path = step.get("path", "")
            content = step.get("content", "")
            result = write_file(path, content)
            state["last_actuator_result"] = result
            state["actuator_log"] = state.get("actuator_log", []) + [{"action": "write_file", "result": result}]
            idx += 1
        
        elif action == "append_file":
            path = step.get("path", "")
            content = step.get("content", "")
            result = append_file(path, content)
            state["last_actuator_result"] = result
            state["actuator_log"] = state.get("actuator_log", []) + [{"action": "append_file", "result": result}]
            idx += 1
        
        elif action == "log_event":
            event_type = step.get("event_type", "info")
            data = step.get("data", {})
            logfile = step.get("logfile", "jarvis.log")
            result = log_event(event_type, data, logfile)
            state["last_actuator_result"] = result
            state["actuator_log"] = state.get("actuator_log", []) + [{"action": "log_event", "result": result}]
            idx += 1
        
        elif action == "notify":
            message = step.get("message", "")
            level = step.get("level", "info")
            result = notify(message, level)
            state["last_actuator_result"] = result
            state["actuator_log"] = state.get("actuator_log", []) + [{"action": "notify", "result": result}]
            idx += 1
        
        elif action == "delete_file":
            path = step.get("path", "")
            result = delete_file(path)
            state["last_actuator_result"] = result
            state["actuator_log"] = state.get("actuator_log", []) + [{"action": "delete_file", "result": result}]
            idx += 1
        
        elif action == "create_directory":
            path = step.get("path", "")
            result = create_directory(path)
            state["last_actuator_result"] = result
            state["actuator_log"] = state.get("actuator_log", []) + [{"action": "create_directory", "result": result}]
            idx += 1
        
        else:
            print(f"[Interpreter] Unknown action: {action}")
            idx += 1
        
        exec_time = time.time() - start_time
        record_execution(sequence_id, idx-1, exec_time)
    
    return {"status": "completed", "final_state": state}