import unittest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from web.app import app

class TestWebInterface(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_memory_page(self):
        response = self.app.get('/memory')
        self.assertEqual(response.status_code, 200)
    
    def test_nodes_page(self):
        response = self.app.get('/nodes')
        self.assertEqual(response.status_code, 200)
    
    def test_tasks_page(self):
        response = self.app.get('/tasks')
        self.assertEqual(response.status_code, 200)
    
    def test_compiler_page(self):
        response = self.app.get('/compiler')
        self.assertEqual(response.status_code, 200)
    
    def test_api_status(self):
        response = self.app.get('/api/status')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
    
    def test_api_execute(self):
        response = self.app.post('/api/execute', 
                                json={'command': 'test', 'mode': 'local'})
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()