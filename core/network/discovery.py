import socket
import json
import time
import threading

class NodeDiscovery:
    def __init__(self):
        self.nodes = {}
        self.running = False
    
    def start(self):
        self.running = True
        print("[Discovery] Started")
    
    def get_active_nodes(self):
        return self.nodes
    
    def discover_nodes(self):
        return list(self.nodes.values())
    
    def stop(self):
        self.running = False
        print("[Discovery] Stopped")

_discovery = NodeDiscovery()

def start_discovery():
    _discovery.start()
    return _discovery

def get_nodes():
    return _discovery.get_active_nodes()

def discover():
    return _discovery.discover_nodes()
