with open(r'C:\Users\Usuario\Documents\TandemWork_Deepseek+ChatGPT\45_Jarfis_format_Platform\Deepseek_answer\20', 'r', encoding='utf-8') as f:
    content = f.read()

# Находим позицию первой {
start_pos = content.find('{')
if start_pos != -1:
    print(f"Найдена {{ на позиции {start_pos}")
    # Покажем контекст
    print("Контекст:")
    print(content[start_pos-50:start_pos+200])
    
    # Сохраняем всё от первой {
    json_content = content[start_pos:]
    with open('build_20_raw.json', 'w', encoding='utf-8') as f:
        f.write(json_content)
    print("✓ build_20_raw.json создан")
else:
    print("{{ не найдена")
