import json
import re
import os
import sys
from pathlib import Path

def extract_files_from_build(build_file_path, target_dir):
    """
    Извлекает файлы из JSON-сборки и создаёт их в target_dir
    """
    print(f"\n📦 Обработка: {build_file_path}")
    
    if not os.path.exists(build_file_path):
        print(f"  ❌ Файл не найден: {build_file_path}")
        return False
    
    with open(build_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Ищем JSON часть (между { и })
    json_match = re.search(r'(\{.*\})', content, re.DOTALL)
    if not json_match:
        print(f"  ⚠️  JSON не найден в {build_file_path}")
        return False
    
    try:
        data = json.loads(json_match.group(1))
        
        # Проверяем структуру
        if 'jarvis_build' not in data:
            print(f"  ⚠️  Нет jarvis_build в {build_file_path}")
            return False
        
        build_data = data['jarvis_build']
        version = build_data.get('version', 'unknown')
        print(f"  📌 Версия: {version}")
        
        if 'files' not in build_data:
            print(f"  ⚠️  Нет files в {build_file_path}")
            return False
        
        files = build_data['files']
        print(f"  📁 Найдено файлов: {len(files)}")
        
        created = 0
        for file_info in files:
            path = file_info.get('path')
            content = file_info.get('content', '')
            
            if not path:
                continue
            
            # Заменяем \n на реальные переносы строк
            file_content = content.replace('\\n', '\n')
            
            # Создаём полный путь
            full_path = os.path.join(target_dir, path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as out_f:
                out_f.write(file_content)
            
            created += 1
        
        print(f"  ✅ Создано файлов: {created}")
        return True
        
    except json.JSONDecodeError as e:
        print(f"  ❌ Ошибка JSON: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Ошибка: {e}")
        return False

def main():
    # Пути
    source_dir = r"C:\Users\Usuario\Documents\TandemWork_Deepseek+ChatGPT\45_Jarfis_format_Platform\Deepseek_answer"
    target_dir = r"C:\Users\Usuario\Jarvis_3.0.1"
    
    # Какие файлы обрабатывать
    start = 7
    end = 19
    
    print("=" * 60)
    print("🛠  EXTRACT BUILDS 7-19")
    print("=" * 60)
    print(f"📂 Источник: {source_dir}")
    print(f"🎯 Цель: {target_dir}")
    print(f"🔢 Диапазон: {start}-{end}")
    print("=" * 60)
    
    success_count = 0
    for i in range(start, end + 1):
        build_file = os.path.join(source_dir, str(i))
        if extract_files_from_build(build_file, target_dir):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"✅ Готово! Обработано успешно: {success_count} из {end-start+1}")
    print("=" * 60)

if __name__ == "__main__":
    main()
