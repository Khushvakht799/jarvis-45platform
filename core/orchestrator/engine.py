import json
import hashlib
from core.engine.interpreter import execute_sequence
from core.metacontrol.memory import add_experience
from core.metacontrol.evolve import adapt_avgr, evolve_sqvgr
from core.life.autonomy import process_learning_command
from core.compiler.bytecode import compile_sequence, disassemble
from core.compiler.optimizer import optimize_graph
from core.compiler.cache import cache_get, cache_put

def text_to_avgr(command_text):
    if command_text == "learn":
        return {
            "intent": {
                "type": "system",
                "command": "learn",
                "params": {}
            }
        }
    
    cmd_lower = command_text.lower()
    
    if "сколько времени" in cmd_lower or "который час" in cmd_lower:
        return {
            "intent": {
                "type": "sensor_query",
                "command": "get_time",
                "params": {}
            }
        }
    
    if "запиши в файл" in cmd_lower:
        parts = command_text.split(" в файл ")
        if len(parts) > 1:
            rest = parts[1].split(" ")
            filename = rest[0]
            content = " ".join(rest[1:])
            return {
                "intent": {
                    "type": "actuator_command",
                    "command": "write_file",
                    "params": {
                        "path": filename,
                        "content": content
                    }
                }
            }
    
    if "случайное число" in cmd_lower:
        return {
            "intent": {
                "type": "sensor_query",
                "command": "random_number",
                "params": {"min": 1, "max": 100}
            }
        }
    
    if "привет" in cmd_lower and "три" in cmd_lower:
        return {
            "intent": {
                "type": "execute_command",
                "command": "output",
                "params": {"text": "привет"},
                "repeat": 3
            }
        }
    
    return {"intent": {"type": "unknown"}}

def avgr_to_sqbvgr(avgr):
    intent = avgr["intent"]
    intent_type = intent["type"]
    command = intent["command"]
    
    if intent_type == "system" and command == "learn":
        result = process_learning_command("learn")
        sqvgr = {"sequence": [{"step": 1, "action": "return", "value": "success"}]}
        bvgr = {"state": {"learning_result": result}}
        return sqvgr, bvgr
    
    if intent_type == "execute_command" and command == "output":
        text = intent["params"]["text"]
        repeat = intent["repeat"]
        
        seq = []
        seq.append({"step": 1, "action": "init_counter", "target": "count", "value": 0})
        seq.append({"step": 2, "action": "loop_start", "condition": f"count < {repeat}"})
        seq.append({"step": 3, "action": "console_output", "value": text})
        seq.append({"step": 4, "action": "increment", "target": "count", "by": 1})
        seq.append({"step": 5, "action": "loop_end"})
        seq.append({"step": 6, "action": "return", "value": "success"})
        
        sqvgr = {"sequence": seq}
        bvgr = {"state": {"count": 0, "output_log": []}}
        return sqvgr, bvgr
    
    elif intent_type == "sensor_query" and command == "get_time":
        seq = [
            {"step": 1, "action": "get_time"},
            {"step": 2, "action": "console_output", "value": "Time checked"},
            {"step": 3, "action": "return", "value": "success"}
        ]
        sqvgr = {"sequence": seq}
        bvgr = {"state": {"output_log": [], "sensor_log": []}}
        return sqvgr, bvgr
    
    elif intent_type == "sensor_query" and command == "random_number":
        min_val = intent["params"].get("min", 1)
        max_val = intent["params"].get("max", 100)
        seq = [
            {"step": 1, "action": "random_number", "min": min_val, "max": max_val},
            {"step": 2, "action": "console_output", "value": "Random number generated"},
            {"step": 3, "action": "return", "value": "success"}
        ]
        sqvgr = {"sequence": seq}
        bvgr = {"state": {"output_log": [], "sensor_log": []}}
        return sqvgr, bvgr
    
    elif intent_type == "actuator_command" and command == "write_file":
        path = intent["params"]["path"]
        content = intent["params"]["content"]
        seq = [
            {"step": 1, "action": "write_file", "path": path, "content": content},
            {"step": 2, "action": "console_output", "value": f"Written to {path}"},
            {"step": 3, "action": "return", "value": "success"}
        ]
        sqvgr = {"sequence": seq}
        bvgr = {"state": {"output_log": [], "actuator_log": []}}
        return sqvgr, bvgr
    
    else:
        return None, None

def run_orchestrator(input_json, sync=False, use_cache=True):
    print("[Orchestrator] Received:", input_json)
    
    try:
        if isinstance(input_json, str):
            data = json.loads(input_json)
        else:
            data = input_json
    except:
        return {"error": "Invalid JSON"}
    
    command = data.get("command", "")
    sequence_id = hashlib.md5(command.encode()).hexdigest()[:8]
    
    avgr = text_to_avgr(command)
    print("[Orchestrator] AVGr (initial):", avgr)
    
    cached = None
    if use_cache:
        cached = cache_get(avgr, {"version": "2.9"})
    
    if cached:
        print("[Orchestrator] Using cached compilation")
        sqvgr = cached["sqvgr"]
        bvgr = cached["bvgr"]
        bytecode = cached.get("bytecode")
        if bytecode:
            print(f"[Orchestrator] Bytecode size: {len(bytecode)} bytes")
    else:
        sqvgr, bvgr = avgr_to_sqbvgr(avgr)
        if sqvgr is None:
            return {"error": "Unknown command"}
        
        sqvgr = optimize_graph(sqvgr)
        
        bytecode, metadata = compile_sequence(sqvgr)
        print(f"[Orchestrator] Compiled to bytecode: {metadata['hash']} ({len(bytecode)} bytes)")
        
        if use_cache:
            cache_put(avgr, {
                "sqvgr": sqvgr,
                "bvgr": bvgr,
                "bytecode": list(bytecode),
                "metadata": metadata
            }, {"version": "2.9"}, metadata)
    
    print("[Orchestrator] SqVGr (optimized):", sqvgr)
    print("[Orchestrator] BVGr (initial):", bvgr)
    
    sqvgr_evolved = evolve_sqvgr(command, sqvgr, {"symptom": {"status": "pending"}}, avgr["intent"])
    if sqvgr_evolved != sqvgr:
        print("[Orchestrator] Using evolved SqVGr")
        sqvgr = sqvgr_evolved
    
    result = execute_sequence(sqvgr["sequence"], bvgr["state"], sequence_id)
    print("[Orchestrator] Execution result:", result)
    
    if avgr["intent"]["type"] == "system":
        givgr = {"gist": {"action": "system", "command": command, "result": "learning"}}
        syvgr = {"symptom": {"status": "success", "learning_result": bvgr["state"].get("learning_result")}}
    elif avgr["intent"]["type"] == "execute_command":
        expected = avgr["intent"].get("repeat", 0)
        actual = len(bvgr["state"].get("output_log", []))
        givgr = {
            "gist": {
                "action": "output",
                "text": command,
                "result": result.get("status", "unknown")
            }
        }
        syvgr = {
            "symptom": {
                "status": result.get("status", "error"),
                "expected": expected,
                "actual": actual,
                "deviation": abs(expected - actual),
                "logs": bvgr["state"].get("output_log", [])
            }
        }
    elif avgr["intent"]["type"] == "sensor_query":
        givgr = {
            "gist": {
                "action": "sensor_query",
                "command": avgr["intent"]["command"],
                "result": result.get("status", "unknown")
            }
        }
        syvgr = {
            "symptom": {
                "status": result.get("status", "error"),
                "sensor_result": bvgr["state"].get("last_sensor_result", {}),
                "logs": bvgr["state"].get("sensor_log", [])
            }
        }
    elif avgr["intent"]["type"] == "actuator_command":
        givgr = {
            "gist": {
                "action": "actuator_command",
                "command": avgr["intent"]["command"],
                "result": result.get("status", "unknown")
            }
        }
        syvgr = {
            "symptom": {
                "status": result.get("status", "error"),
                "actuator_result": bvgr["state"].get("last_actuator_result", {}),
                "logs": bvgr["state"].get("actuator_log", [])
            }
        }
    else:
        givgr = {"gist": {"result": "unknown"}}
        syvgr = {"symptom": {"status": "unknown"}}
    
    print("[Orchestrator] GiVGr:", givgr)
    print("[Orchestrator] SyVGr:", syvgr)
    
    add_experience(command, avgr, sqvgr, bvgr, givgr, syvgr)
    
    avgr_adapted = adapt_avgr(command, avgr, syvgr)
    if avgr_adapted != avgr:
        print("[Orchestrator] AVGr adapted for future runs")
    
    if sync:
        try:
            from core.network.client import sync_memory
            sync_memory()
        except:
            pass
    
    return {
        "status": "ok",
        "givgr": givgr,
        "syvgr": syvgr,
        "final_state": bvgr["state"],
        "sequence_used": sqvgr,
        "bytecode_hash": metadata.get("hash") if not cached else None
    }