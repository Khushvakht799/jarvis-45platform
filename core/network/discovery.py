import socket
import json
import time
import threading

class NodeDiscovery:
    def __init__(self):
        self.nodes = {}
    
    def get_active_nodes(self):
        return self.nodes

_discovery = NodeDiscovery()

def get_nodes():
    return _discovery.get_active_nodes()
