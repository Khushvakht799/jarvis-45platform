import unittest
import sys
import os
import json
import time
import threading
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.network.discovery import NodeDiscovery, get_nodes
from core.network.server import app

class TestNetwork(unittest.TestCase):
    
    def test_discovery_init(self):
        discovery = NodeDiscovery()
        self.assertIsNotNone(discovery)
    
    def test_server_app_exists(self):
        self.assertIsNotNone(app)
    
    def test_server_routes(self):
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        self.assertIn('/execute', ''.join(routes))
        self.assertIn('/result/<task_id>', ''.join(routes))
        self.assertIn('/stats', ''.join(routes))
        self.assertIn('/health', ''.join(routes))

class TestServerEndpoints(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_endpoint(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_stats_endpoint(self):
        response = self.app.get('/stats')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)

if __name__ == '__main__':
    unittest.main()