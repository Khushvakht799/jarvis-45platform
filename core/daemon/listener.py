import sys
import json
import time
import argparse
from core.orchestrator.engine import run_orchestrator

def listen_stdin(sync=False, autonomous=False, no_cache=False, distributed=False):
    print("[Daemon] Listening for commands on stdin. Type 'exit' to quit.")
    use_cache = not no_cache
    
    if sync:
        print("[Daemon] Network sync enabled")
        from core.network.client import start_sync_loop
        start_sync_loop()
    
    if autonomous:
        print("[Daemon] Autonomous mode enabled")
        from core.life.autonomy import start_autonomy
        start_autonomy()
    
    if distributed:
        print("[Daemon] Distributed mode enabled")
        from core.orchestrator.distributed import start_distributed
        start_distributed()
    
    print(f"[Daemon] Compiler cache: {'enabled' if use_cache else 'disabled'}")
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                time.sleep(0.1)
                continue
            
            cmd = line.strip()
            if cmd.lower() == 'exit':
                print("[Daemon] Shutting down.")
                break
            
            if not cmd:
                continue
            
            if cmd.startswith('{') and cmd.endswith('}'):
                input_json = json.loads(cmd)
            else:
                input_json = {"command": cmd}
            
            if distributed and cmd.startswith("dist:"):
                # Распределённое выполнение
                from core.orchestrator.distributed import execute_distributed
                actual_cmd = cmd[5:]
                result = execute_distributed(actual_cmd)
            else:
                result = run_orchestrator(input_json, sync=sync, use_cache=use_cache)
            
            print("[Daemon] Result:", json.dumps(result, ensure_ascii=False, indent=2))
            print("---")
        except KeyboardInterrupt:
            print("
[Daemon] Interrupted. Exiting.")
            break
        except Exception as e:
            print(f"[Daemon] Error: {e}")

def listen_file(filepath, sync=False, autonomous=False, no_cache=False, distributed=False):
    print(f"[Daemon] Watching file: {filepath}")
    use_cache = not no_cache
    
    if sync:
        print("[Daemon] Network sync enabled")
        from core.network.client import start_sync_loop
        start_sync_loop()
    
    if autonomous:
        print("[Daemon] Autonomous mode enabled")
        from core.life.autonomy import start_autonomy
        start_autonomy()
    
    if distributed:
        print("[Daemon] Distributed mode enabled")
        from core.orchestrator.distributed import start_distributed
        start_distributed()
    
    print(f"[Daemon] Compiler cache: {'enabled' if use_cache else 'disabled'}")
    
    last_content = ""
    while True:
        try:
            with open(filepath, 'r') as f:
                content = f.read().strip()
            if content and content != last_content:
                print(f"[Daemon] New content detected")
                last_content = content
                if content.startswith('{') and content.endswith('}'):
                    input_json = json.loads(content)
                else:
                    input_json = {"command": content}
                
                if distributed and content.startswith("dist:"):
                    from core.orchestrator.distributed import execute_distributed
                    actual_cmd = content[5:]
                    result = execute_distributed(actual_cmd)
                else:
                    result = run_orchestrator(input_json, sync=sync, use_cache=use_cache)
                
                print("[Daemon] Result:", json.dumps(result, ensure_ascii=False, indent=2))
                print("---")
            time.sleep(1)
        except FileNotFoundError:
            print(f"[Daemon] File not found: {filepath}, waiting...")
            time.sleep(2)
        except Exception as e:
            print(f"[Daemon] Error: {e}")
            time.sleep(1)

if name == "main":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Watch file instead of stdin")
    parser.add_argument("--sync", action="store_true", help="Enable network sync")
    parser.add_argument("--autonomous", action="store_true", help="Enable autonomous mode")
    parser.add_argument("--no-cache", action="store_true", help="Disable compiler cache")
    parser.add_argument("--distributed", action="store_true", help="Enable distributed mode")
    args = parser.parse_args()
    
    if args.file:
        listen_file(args.file, sync=args.sync, autonomous=args.autonomous, 
                   no_cache=args.no_cache, distributed=args.distributed)
    else:
        listen_stdin(sync=args.sync, autonomous=args.autonomous, 
                    no_cache=args.no_cache, distributed=args.distributed)