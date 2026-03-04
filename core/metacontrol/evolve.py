from core.metacontrol.memory import find_similar_commands, get_best_sequence, get_pattern_stats
from core.metacontrol.optimizer import optimize_sequence
from core.metacontrol.vectorizer import avgr_to_vector, cosine_similarity

def adapt_avgr(command, avgr, syvgr):
    if syvgr["symptom"].get("deviation", 0) != 0:
        print("[Evolve] Deviation detected, adapting AVGr...")
        similar = find_similar_commands(command)
        if similar:
            current_vec = avgr_to_vector(avgr)
            best_sim = 0
            best_avgr = None
            for exp in similar:
                if exp["syvgr"]["symptom"]["status"] == "success":
                    sim = cosine_similarity(current_vec, exp["avgr_vector"])
                    if sim > best_sim:
                        best_sim = sim
                        best_avgr = exp["avgr"]
            if best_avgr and best_sim > 0.7:
                if "repeat" in best_avgr["intent"]:
                    avgr["intent"]["repeat"] = best_avgr["intent"]["repeat"]
                    print(f"[Evolve] Adjusted repeat to {avgr['intent']['repeat']} (similarity: {best_sim:.2f})")
    return avgr

def evolve_sqvgr(command, sqvgr, syvgr, intent):
    best = get_best_sequence(command)
    if best:
        print("[Evolve] Found better sequence in memory, applying")
        return best
    
    optimized = optimize_sequence(sqvgr["sequence"], intent)
    
    stats = get_pattern_stats(intent["type"], intent["command"])
    if stats.get("count", 0) > 5:
        avg_len = stats.get("avg_length", 0)
        if len(optimized["sequence"]) > avg_len * 1.2:
            print(f"[Evolve] Current sequence longer than average ({len(optimized['sequence'])} > {avg_len:.1f}), looking for shorter pattern")
    
    return optimized