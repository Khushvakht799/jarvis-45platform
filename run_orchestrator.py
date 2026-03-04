#!/usr/bin/env python3
"""
Jarvis Orchestrator Launcher
"""
from core.orchestrator.engine import run_orchestrator

if __name__ == "__main__":
    test_input = {"command": "скажи привет три раза"}
    result = run_orchestrator(test_input)
    print("\nFinal result:", result)
