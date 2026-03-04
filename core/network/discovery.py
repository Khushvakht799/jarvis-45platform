import socket
import json
import time
import threading
from collections import defaultdict

class NodeDiscovery:
    def init(self, multicast_group='224.1.1.1', port=5005):
        self.multicast_group = multicast_group
        self.port = port
        self.nodes = {}  # node_id -> {address, last_seen, capabilities}
        self.running = False
        self.sock = None
        self.node_id = socket.gethostname() + ":" + str(port)
    
    def start(self):
        """Запускает обнаружение узлов"""
        self.running = True
        # Создаём сокет для multicast
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Подписываемся на multicast группу
        mreq = socket.inet_aton(self.multicast_group) + socket.inet_pton(socket.AF_INET, '0.0.0.0')
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
        # Привязываемся к порту
        self.sock.bind(('', self.port))
        self.sock.settimeout(1.0)
        
        # Запускаем потоки
        self.listener_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listener_thread.start()
        
        self.announcer_thread = threading.Thread(target=self._announce_loop, daemon=True)
        self.announcer_thread.start()
        
        print(f"[Discovery] Started on {self.multicast_group}:{self.port}")
    
    def _announce_loop(self):
        """Периодически объявляет о себе"""
        while self.running:
            try:
                message = json.dumps({
                    "type": "announce",
                    "node_id": self.node_id,
                    "timestamp": time.time(),
                    "capabilities": self._get_capabilities()
                })
                self.sock.sendto(message.encode(), (self.multicast_group, self.port))
            except:
                pass
            time.sleep(5)
    
    def _listen_loop(self):
        """Слушает объявления других узлов"""
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                message = json.loads(data.decode())
                
                if message["type"] == "announce":
                    node_id = message["node_id"]
                    if node_id != self.node_id:
                        self.nodes[node_id] = {
                            "address": addr[0],
                            "port": self.port,
                            "last_seen": time.time(),
                            "capabilities": message.get("capabilities", {})
                        }
                        print(f"[Discovery] Found node {node_id} at {addr[0]}")
                
                elif message["type"] == "query":
                    # Ответ на запрос
                    response = json.dumps({
                        "type": "response",
                        "node_id": self.node_id,
                        "timestamp": time.time(),
                        "capabilities": self._get_capabilities()
                    })
                    self.sock.sendto(response.encode(), addr)
                
                elif message["type"] == "response":
                    node_id = message["node_id"]
                    if node_id != self.node_id:
                        self.nodes[node_id] = {
                            "address": addr[0],
                            "port": self.port,
                            "last_seen": time.time(),
                            "capabilities": message.get("capabilities", {})
                        }
            except socket.timeout:
                pass
            except Exception as e:
                print(f"[Discovery] Error: {e}")
    
    def _get_capabilities(self):
        """Возвращает возможности узла"""
        return {
            "interpreter": True,
            "jit": True,
            "compiler": True,
            "physics": True,
            "autonomy": True,
            "max_tasks": 5
        }
    
    def discover_nodes(self):
        """Активный поиск узлов"""
        try:
            message = json.dumps({
                "type": "query",
                "node_id": self.node_id,
                "timestamp": time.time()
            })
            self.sock.sendto(message.encode(), (self.multicast_group, self.port))
        except:
            pass
        return list(self.nodes.values())
    
    def get_active_nodes(self, max_age=30):
        """Возвращает активные узлы"""
        now = time.time()
        return {nid: info for nid, info in self.nodes.items() 
                if now - info["last_seen"] < max_age}
    
    def stop(self):
        self.running = False
        if self.sock:
            self.sock.close()
        print("[Discovery] Stopped")

_discovery = NodeDiscovery()

def start_discovery():
    _discovery.start()
    return _discovery

def get_nodes():
    return _discovery.get_active_nodes()

def discover():
    return _discovery.discover_nodes()