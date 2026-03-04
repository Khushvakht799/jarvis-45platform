import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.compiler.bytecode import compile_sequence, disassemble
from core.compiler.cache import CompilerCache, cache_stats
from core.compiler.optimizer import optimize_sequence

class TestCompiler(unittest.TestCase):
    
    def setUp(self):
        self.test_sequence = {
            "sequence": [
                {"step": 1, "action": "console_output", "value": "test"},
                {"step": 2, "action": "return", "value": "success"}
            ]
        }
    
    def test_compile_sequence(self):
        bytecode, metadata = compile_sequence(self.test_sequence)
        self.assertIsNotNone(bytecode)
        self.assertIsNotNone(metadata)
        self.assertIn('hash', metadata)
    
    def test_disassemble(self):
        bytecode, metadata = compile_sequence(self.test_sequence)
        instructions = disassemble(bytecode)
        self.assertGreater(len(instructions), 0)
    
    def test_cache(self):
        cache = CompilerCache()
        stats = cache.get_stats()
        self.assertIn('hits', stats)
        self.assertIn('misses', stats)
    
    def test_optimizer(self):
        optimized = optimize_sequence(self.test_sequence, {})
        self.assertIsNotNone(optimized)

if __name__ == '__main__':
    unittest.main()