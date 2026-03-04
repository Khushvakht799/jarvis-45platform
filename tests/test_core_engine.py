import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.framework.output import console_output
from core.engine.interpreter import execute_sequence
from core.orchestrator.engine import text_to_avgr, avgr_to_sqbvgr, run_orchestrator

class TestCoreEngine(unittest.TestCase):
    
    def test_console_output(self):
        result = console_output("test")
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(result['output'], 'test')
    
    def test_execute_sequence_basic(self):
        sequence = {
            "sequence": [
                {"step": 1, "action": "console_output", "value": "test"},
                {"step": 2, "action": "return", "value": "success"}
            ]
        }
        state = {"output_log": []}
        result = execute_sequence(sequence["sequence"], state)
        self.assertEqual(result['status'], 'success')
        self.assertIn('test', state['output_log'])
    
    def test_execute_sequence_loop(self):
        sequence = {
            "sequence": [
                {"step": 1, "action": "init_counter", "target": "count", "value": 0},
                {"step": 2, "action": "loop_start", "condition": "count < 3"},
                {"step": 3, "action": "console_output", "value": "loop"},
                {"step": 4, "action": "increment", "target": "count", "by": 1},
                {"step": 5, "action": "loop_end"},
                {"step": 6, "action": "return", "value": "success"}
            ]
        }
        state = {"count": 0, "output_log": []}
        result = execute_sequence(sequence["sequence"], state)
        self.assertEqual(result['status'], 'success')
        self.assertEqual(len(state['output_log']), 3)
        self.assertEqual(state['count'], 3)
    
    def test_text_to_avgr(self):
        result = text_to_avgr("скажи привет три раза")
        self.assertEqual(result['intent']['type'], 'execute_command')
        self.assertEqual(result['intent']['repeat'], 3)
    
    def test_avgr_to_sqbvgr(self):
        avgr = {
            "intent": {
                "type": "execute_command",
                "command": "output",
                "params": {"text": "test"},
                "repeat": 2
            }
        }
        sqvgr, bvgr = avgr_to_sqbvgr(avgr)
        self.assertIsNotNone(sqvgr)
        self.assertEqual(len(sqvgr['sequence']), 6)
        self.assertEqual(bvgr['state']['count'], 0)
    
    def test_run_orchestrator(self):
        result = run_orchestrator({"command": "скажи привет три раза"})
        self.assertEqual(result['status'], 'ok')
        self.assertIn('givgr', result)
        self.assertIn('syvgr', result)

if __name__ == '__main__':
    unittest.main()