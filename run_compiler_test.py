from core.compiler.bytecode import compile_sequence, disassemble
from core.compiler.optimizer import optimize_graph
from core.compiler.cache import cache_get, cache_put, cache_stats

# Тестовая последовательность
test_sqvgr = {
    "sequence": [
        {"step": 1, "action": "init_counter", "target": "count", "value": 0},
        {"step": 2, "action": "loop_start", "condition": "count < 3"},
        {"step": 3, "action": "console_output", "value": "привет"},
        {"step": 4, "action": "increment", "target": "count", "by": 1},
        {"step": 5, "action": "loop_end"},
        {"step": 6, "action": "return", "value": "success"}
    ]
}

print("=== Compiler Test ===")

# Оптимизация
optimized = optimize_graph(test_sqvgr)
print(f"Optimized: {len(optimized['sequence'])} steps (was {len(test_sqvgr['sequence'])})")

# Компиляция
bytecode, metadata = compile_sequence(test_sqvgr)
print(f"Bytecode: {len(bytecode)} bytes, hash: {metadata['hash']}")

# Дизассемблирование
instructions = disassemble(bytecode)
print("
Disassembly:")
for instr in instructions:
    print(f"  {instr['offset']:04x}: {instr['action']}")

# Тест кэша
print("
=== Cache Test ===")
avgr = {"intent": {"type": "execute_command", "command": "output", "params": {"text": "привет"}, "repeat": 3}}
cache_put(avgr, {"sqvgr": test_sqvgr, "bvgr": {}}, {"version": "test"})
cached = cache_get(avgr, {"version": "test"})
print(f"Cache hit: {cached is not None}")
print(f"Cache stats: {cache_stats()}")