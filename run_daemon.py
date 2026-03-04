#!/usr/bin/env python3
\"\"\"
Jarvis Daemon Launcher
\"\"\"
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from core.daemon.listener import listen_stdin
except ImportError as e:
    print(f"Error importing daemon: {e}")
    print("Make sure core.daemon.listener exists")
    sys.exit(1)

if __name__ == "__main__":
    sync = "--sync" in sys.argv
    autonomous = "--autonomous" in sys.argv
    no_cache = "--no-cache" in sys.argv
    distributed = "--distributed" in sys.argv
    
    print("=" * 60)
    print("Jarvis 3.0.1 Daemon")
    print("=" * 60)
    print(f"  sync={sync}, autonomous={autonomous}, cache={not no_cache}, distributed={distributed}")
    print("=" * 60)
    
    listen_stdin(sync=sync, autonomous=autonomous, no_cache=no_cache, distributed=distributed)
