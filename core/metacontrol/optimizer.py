def optimize_sequence(sequence, intent):
    print("[Optimizer] Analyzing sequence for optimization...")
    
    new_seq = sequence.copy()
    
    i = 0
    while i < len(new_seq) - 1:
        if new_seq[i]["action"] == "console_output" and new_seq[i+1]["action"] == "console_output":
            if new_seq[i]["value"] == new_seq[i+1]["value"]:
                print(f"[Optimizer] Found repeated outputs at steps {i+1}, {i+2}")
                j = i
                count = 0
                while j < len(new_seq) and new_seq[j]["action"] == "console_output" and new_seq[j]["value"] == new_seq[i]["value"]:
                    count += 1
                    j += 1
                
                if count > 2:
                    print(f"[Optimizer] Replacing {count} repeats with loop")
                    del new_seq[i:j]
                    loop_start = {
                        "step": i+1,
                        "action": "loop_start",
                        "condition": f"count < {count}"
                    }
                    loop_body = {
                        "step": i+2,
                        "action": "console_output",
                        "value": new_seq[i]["value"]
                    }
                    loop_increment = {
                        "step": i+3,
                        "action": "increment",
                        "target": "count",
                        "by": 1
                    }
                    loop_end = {
                        "step": i+4,
                        "action": "loop_end"
                    }
                    new_seq[i:i] = [loop_start, loop_body, loop_increment, loop_end]
                    for idx, step in enumerate(new_seq):
                        step["step"] = idx + 1
                    break
        i += 1
    
    init_targets = set()
    i = 0
    while i < len(new_seq):
        if new_seq[i]["action"] == "init_counter":
            target = new_seq[i]["target"]
            if target in init_targets:
                print(f"[Optimizer] Removing duplicate init_counter for {target}")
                del new_seq[i]
                continue
            else:
                init_targets.add(target)
        i += 1
    
    for idx, step in enumerate(new_seq):
        step["step"] = idx + 1
    
    if new_seq != sequence:
        print(f"[Optimizer] Sequence optimized: {len(sequence)} -> {len(new_seq)} steps")
    else:
        print("[Optimizer] No optimizations applied")
    
    return {"sequence": new_seq}