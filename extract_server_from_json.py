import json

try:
    with open('build_20_clean.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if 'jarvis_build' in data and 'files' in data['jarvis_build']:
        for file in data['jarvis_build']['files']:
            if file['path'] == 'core/network/server.py':
                print("✓ Найден server.py")
                content = file['content'].replace('\\n', '\n')
                with open('core/network/server.py', 'w', encoding='utf-8') as sf:
                    sf.write(content)
                print("✓ core/network/server.py создан")
                break
        else:
            print("server.py не найден в списке файлов")
    else:
        print("Нет jarvis_build или files в JSON")
except Exception as e:
    print(f"Ошибка: {e}")
