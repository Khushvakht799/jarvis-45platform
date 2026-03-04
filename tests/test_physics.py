import unittest
import sys
import os
import tempfile
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.physics.sensors import get_time, read_file, file_exists, random_number
from core.physics.actuators import write_file, delete_file

class TestPhysics(unittest.TestCase):
    
    def test_get_time(self):
        result = get_time()
        self.assertIn('timestamp', result)
        self.assertIn('hour', result)
    
    def test_random_number(self):
        result = random_number(1, 10)
        self.assertIn('value', result)
        self.assertGreaterEqual(result['value'], 1)
        self.assertLessEqual(result['value'], 10)
    
    def test_file_operations(self):
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Write
            write_result = write_file(tmp_path, "test content")
            self.assertEqual(write_result['status'], 'ok')
            
            # Exists
            exists_result = file_exists(tmp_path)
            self.assertTrue(exists_result['exists'])
            
            # Read
            read_result = read_file(tmp_path)
            self.assertEqual(read_result['status'], 'ok')
            self.assertEqual(read_result['content'], "test content")
        finally:
            # Cleanup
            delete_file(tmp_path)

if __name__ == '__main__':
    unittest.main()