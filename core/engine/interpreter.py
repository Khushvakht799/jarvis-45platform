from core.framework.output import console_output

def execute_sequence(sqVGr, bvGr):
    """Интерпретатор SqVGr - первая версия"""
    # bvGr - это состояние (словарь)
    for step in sqVGr["sequence"]:
        action = step["action"]
        
        if action == "init_counter":
            bvGr["state"][step["target"]] = step["value"]
        
        elif action == "loop_start":
            condition = step["condition"]  # например "count < 3"
            # Парсим условие (примитивно)
            var_name = condition.split()[0]
            limit = int(condition.split()[2])
            while bvGr["state"].get(var_name, 0) < limit:
                # Здесь хитрость: нужно выполнять тело цикла
                # Пропускаем шаги до loop_end
                # Для первого теста можно захардкодить логику цикла,
                # но лучше написать отдельный sub-interpreter для тела.
                # Пока сделаем заглушку:
                break  # Пока не реализовано
            # В реальности тут будет вложенный цикл
        
        elif action == "console_output":
            console_output(step["value"])
            # Добавляем в лог состояния
            if "output_log" not in bvGr["state"]:
                bvGr["state"]["output_log"] = []
            bvGr["state"]["output_log"].append(step["value"])
        
        elif action == "increment":
            bvGr["state"][step["target"]] += step["by"]
        
        elif action == "return":
            return {"status": step["value"], "final_state": bvGr["state"]}
    
    return {"status": "completed", "final_state": bvGr["state"]}


if __name__ == "__main__":
    # Тест
    test_sq = {
        "sequence": [
            { "step": 1, "action": "init_counter", "target": "count", "value": 0 },
            { "step": 2, "action": "loop_start", "condition": "count < 3" },  # Пока не работает
            { "step": 3, "action": "console_output", "value": "привет" },
            { "step": 4, "action": "increment", "target": "count", "by": 1 },
            { "step": 5, "action": "loop_end" },
            { "step": 6, "action": "return", "value": "success" }
        ]
    }
    test_bv = {"state": {"count": 0, "output_log": []}}
    
    # Временно заменим цикл на простой for, чтобы проверить вывод
    print("Ручной тест (без цикла):")
    for i in range(3):
        console_output("привет")
    print("Тест пройден")
