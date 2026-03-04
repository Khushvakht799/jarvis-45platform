# extract_release.py
import json
import os

with open('release_3.0.1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

files = data['jarvis_build']['files']

for file_info in files:
    path = file_info['path']
    content = file_info['content']
    
    dirname = os.path.dirname(path)
    if dirname:
        os.makedirs(dirname, exist_ok=True)
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {path}")