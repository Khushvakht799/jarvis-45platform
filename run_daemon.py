from core.daemon.listener import listen_stdin
import sys

if name == "main":
    sync = "--sync" in sys.argv
    autonomous = "--autonomous" in sys.argv
    no_cache = "--no-cache" in sys.argv
    distributed = "--distributed" in sys.argv
    print(f"Starting Jarvis 2.9.1 Daemon with Distributed Orchestration")
    print(f"  sync={sync}, autonomous={autonomous}, cache={not no_cache}, distributed={distributed}")
    listen_stdin(sync=sync, autonomous=autonomous, no_cache=no_cache, distributed=distributed)