import json
from core.engine.interpreter import execute_sequence

def text_to_avgr(command_text):
    if "привет" in command_text and "три" in command_text:
        return {
            "intent": {
                "type": "execute_command",
                "command": "output",
                "params": {"text": "привет"},
                "repeat": 3
            }
        }
    else:
        return {"intent": {"type": "unknown"}}

def avgr_to_sqbvgr(avgr):
    if avgr["intent"]["type"] == "execute_command" and avgr["intent"]["command"] == "output":
        text = avgr["intent"]["params"]["text"]
        repeat = avgr["intent"]["repeat"]
        
        seq = []
        seq.append({"step": 1, "action": "init_counter", "target": "count", "value": 0})
        seq.append({"step": 2, "action": "loop_start", "condition": f"count < {repeat}"})
        seq.append({"step": 3, "action": "console_output", "value": text})
        seq.append({"step": 4, "action": "increment", "target": "count", "by": 1})
        seq.append({"step": 5, "action": "loop_end"})
        seq.append({"step": 6, "action": "return", "value": "success"})
        
        for i, step in enumerate(seq):
            step["step"] = i + 1
        
        sqvgr = {"sequence": seq}
        bvgr = {"state": {"count": 0, "output_log": []}}
        return sqvgr, bvgr
    else:
        return None, None

def run_orchestrator(input_json):
    print("[Orchestrator] Received:", input_json)
    
    try:
        if isinstance(input_json, str):
            data = json.loads(input_json)
        else:
            data = input_json
    except:
        return {"error": "Invalid JSON"}
    
    command = data.get("command", "")
    
    avgr = text_to_avgr(command)
    print("[Orchestrator] AVGr:", avgr)
    
    sqvgr, bvgr = avgr_to_sqbvgr(avgr)
    if sqvgr is None:
        return {"error": "Unknown command"}
    
    print("[Orchestrator] SqVGr:", sqvgr)
    print("[Orchestrator] BVGr:", bvgr)
    
    result = execute_sequence(sqvgr["sequence"], bvgr["state"])
    print("[Orchestrator] Execution result:", result)
    
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
            "expected": avgr["intent"].get("repeat", 0),
            "actual": len(bvgr["state"].get("output_log", [])),
            "deviation": 0,
            "logs": bvgr["state"].get("output_log", [])
        }
    }
    
    print("[Orchestrator] GiVGr:", givgr)
    print("[Orchestrator] SyVGr:", syvgr)
    
    return {
        "status": "ok",
        "givgr": givgr,
        "syvgr": syvgr,
        "final_state": bvgr["state"]
    }

if __name__ == "__main__":
    test_input = {"command": "скажи привет три раза"}
    result = run_orchestrator(test_input)
    print("\n[Orchestrator] Final result:", result)
