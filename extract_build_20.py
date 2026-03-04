import json
import re
import os

def extract_json_objects(content):
    """Извлекает все JSON объекты из текста"""
    objects = []
    stack = []
    start_idx = -1
    
    for i, char in enumerate(content):
        if char == '{':
            if not stack:
                start_idx = i
            stack.append('{')
        elif char == '}':
            if stack:
                stack.pop()
                if not stack and start_idx != -1:
                    json_str = content[start_idx:i+1]
                    try:
                        obj = json.loads(json_str)
                        objects.append(obj)
                    except:
                        pass
                    start_idx = -1
    return objects

def extract_files_from_build(build_data, target_dir):
    """Извлекает файлы из одной сборки"""
    if 'jarvis_build' in build_data:
        build_data = build_data['jarvis_build']
    
    version = build_data.get('version', 'unknown')
    files = build_data.get('files', [])
    
    if not files:
        return 0, version
    
    print(f"\n📦 Версия {version}: {len(files)} файлов")
    
    created = 0
    for file_info in files:
        path = file_info.get('path')
        content = file_info.get('content', '')
        
        if not path:
            continue
        
        file_content = content.replace('\\n', '\n')
        full_path = os.path.join(target_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        print(f"  ✅ {path}")
        created += 1
    
    return created, version

def main():
    source_file = r"C:\Users\Usuario\Jarvis_3.0.1\build_20.json"
    target_dir = r"C:\Users\Usuario\Jarvis_3.0.1"
    
    print("=" * 60)
    print("🔍 ПОИСК ВСЕХ СБОРОК В BUILD_20.JSON")
    print("=" * 60)
    
    with open(source_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("Извлечение JSON объектов...")
    objects = extract_json_objects(content)
    print(f"Найдено JSON объектов: {len(objects)}")
    
    total_files = 0
    versions_found = []
    
    for i, obj in enumerate(objects):
        try:
            created, version = extract_files_from_build(obj, target_dir)
            if created > 0:
                total_files += created
                versions_found.append(f"{version} ({created} файлов)")
        except:
            continue
    
    print("\n" + "=" * 60)
    print("✅ РЕЗУЛЬТАТ:")
    print(f"   Найдено версий: {len(versions_found)}")
    for v in versions_found:
        print(f"     • {v}")
    print(f"   Всего создано файлов: {total_files}")
    print("=" * 60)

if __name__ == "__main__":
    main()
