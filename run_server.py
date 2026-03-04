#!/usr/bin/env python3
\"\"\"
Jarvis Network Server Launcher
\"\"\"
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.network.server import app
except ImportError as e:
    print(f"Error importing network server: {e}")
    print("Make sure core.network.server exists")
    sys.exit(1)

if __name__ == "__main__":
    print("=" * 60)
    print("Jarvis Network Server")
    print("=" * 60)
    print("Server running on http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
