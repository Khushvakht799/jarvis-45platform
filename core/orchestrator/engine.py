import json
from core.engine.interpreter import execute_sequence

def run_orchestrator(input_json, sync=False, use_cache=True):
    \"\"\"Минимальный оркестратор\"\"\"
    print(f"[Orchestrator] Received: {input_json}")
    
    if isinstance(input_json, str):
        try:
            data = json.loads(input_json)
        except:
            return {"error": "Invalid JSON"}
    else:
        data = input_json
    
    command = data.get("command", "")
    
    # Минимальная последовательность
    sqvgr = {
        "sequence": [
            {"step": 1, "action": "console_output", "value": f"Executing: {command}"},
            {"step": 2, "action": "return", "value": "success"}
        ]
    }
    bvgr = {"state": {"output_log": []}}
    
    result = execute_sequence(sqvgr["sequence"], bvgr["state"])
    
    return {
        "status": "ok",
        "result": result,
        "final_state": bvgr["state"]
    }
