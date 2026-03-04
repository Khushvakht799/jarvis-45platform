from core.network.discovery import start_discovery, get_nodes
import time

print("Starting node discovery test")
discovery = start_discovery()

try:
    for i in range(10):
        nodes = get_nodes()
        print(f"Active nodes: {len(nodes)}")
        for nid, info in nodes.items():
            print(f"  {nid}: {info['address']}")
        time.sleep(5)
except KeyboardInterrupt:
    print("Stopping")
finally:
    discovery.stop()