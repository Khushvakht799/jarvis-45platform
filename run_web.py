#!/usr/bin/env python3
"""
Jarvis Web UI Launcher
"""
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from web.app import app
except ImportError as e:
    print(f"Error importing web.app: {e}")
    print("Make sure the web module exists and has app.py")
    sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("Jarvis 3.0.1 Web Interface")
    print("=" * 60)
    print("Access the dashboard at: http://localhost:8080")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8080, debug=True)
