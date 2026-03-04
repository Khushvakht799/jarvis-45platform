#!/usr/bin/env python3
"""
Jarvis Web UI Launcher
"""
import sys
import os

# Добавляем корневую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(file)))

from web.app import app

if name == "main":
    print("=" * 60)
    print("Jarvis 3.0 Web Interface")
    print("=" * 60)
    print("Access the dashboard at: http://localhost:8080")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(host='0.0.0.0', port=8080, debug=True)