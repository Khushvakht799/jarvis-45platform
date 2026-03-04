from core.framework.output import console_output

def execute_sequence(sqVGr, bvGr):
    for step in sqVGr["sequence"]:
        action = step["action"]
        if action == "init_counter":
            bvGr["state"][step["target"]] = step["value"]
        elif action == "console_output":
            console_output(step["value"])
            if "output_log" not in bvGr["state"]:
                bvGr["state"]["output_log"] = []
            bvGr["state"]["output_log"].append(step["value"])
        elif action == "increment":
            bvGr["state"][step["target"]] += step["by"]
        elif action == "return":
            return {"status": step["value"], "final_state": bvGr["state"]}
    return {"status": "completed", "final_state": bvGr["state"]}

if __name__ == "__main__":
    test_sq = {
        "sequence": [
            {"step": 1, "action": "init_counter", "target": "count", "value": 0},
            {"step": 2, "action": "console_output", "value": "привет"},
            {"step": 3, "action": "increment", "target": "count", "by": 1},
            {"step": 4, "action": "console_output", "value": "привет"},
            {"step": 5, "action": "increment", "target": "count", "by": 1},
            {"step": 6, "action": "console_output", "value": "привет"},
            {"step": 7, "action": "return", "value": "success"}
        ]
    }
    test_bv = {"state": {"count": 0, "output_log": []}}
    result = execute_sequence(test_sq, test_bv)
    print("Test result:", result)
