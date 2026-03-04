# extract_analysis.py
import json
import os

print("=" * 60)
print("📦 EXTRACT JARVIS ANALYSIS")
print("=" * 60)

# Читаем файл анализа
with open('jarvis_analysis.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Извлекаем файлы
if 'jarvis_build' in data and 'files' in data['jarvis_build']:
    files = data['jarvis_build']['files']
    print(f"📁 Найдено файлов: {len(files)}")
    
    created = 0
    skipped = 0
    
    for file_info in files:
        path = file_info.get('path', '')
        content = file_info.get('content', '')
        
        if not path:
            print(f"  ⚠️  Пропущен: нет пути")
            skipped += 1
            continue
        
        # Если content словарь, конвертируем в JSON строку
        if isinstance(content, dict):
            content = json.dumps(content, indent=2, ensure_ascii=False)
        
        # Создаём папку только если есть директория
        dirname = os.path.dirname(path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        
        # Записываем файл
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ {path}")
            created += 1
        except Exception as e:
            print(f"  ❌ {path}: {e}")
            skipped += 1
    
    print("\n" + "=" * 60)
    print(f"✅ РЕЗУЛЬТАТ:")
    print(f"   Создано файлов: {created}")
    print(f"   Пропущено: {skipped}")
    print("=" * 60)
else:
    print("❌ Нет файлов для извлечения")