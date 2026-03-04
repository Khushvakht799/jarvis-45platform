import re

with open(r'C:\Users\Usuario\Documents\TandemWork_Deepseek+ChatGPT\45_Jarfis_format_Platform\Deepseek_answer\20', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Ищем строку с "jarvis_build"
json_start = None
json_lines = []
in_json = False
brace_count = 0

for i, line in enumerate(lines):
    if '"jarvis_build"' in line and not in_json:
        in_json = True
        json_start = i
        print(f"Найдено начало JSON на строке {i+1}")
    
    if in_json:
        json_lines.append(line)
        brace_count += line.count('{')
        brace_count -= line.count('}')
        if brace_count == 0 and json_lines:
            # Нашли конец JSON
            print(f"Конец JSON на строке {i+1}")
            break

if json_lines:
    json_str = ''.join(json_lines)
    # Сохраняем в файл
    with open('build_20_clean.json', 'w', encoding='utf-8') as f:
        f.write(json_str)
    print("✓ build_20_clean.json создан")
    print(f"Размер: {len(json_str)} символов")
else:
    print("JSON не найден")
