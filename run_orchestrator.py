from core.orchestrator.engine import run_orchestrator

# Тестовый запуск
input_command = {"command": "скажи привет три раза"}
result = run_orchestrator(input_command)
print("\n[Launcher] Final result:", result)
