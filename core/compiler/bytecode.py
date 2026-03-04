import hashlib
import json

class BytecodeCompiler:
    def init(self):
        self.opcodes = {
            "init_counter": 0x01,
            "console_output": 0x02,
            "increment": 0x03,
            "loop_start": 0x10,
            "loop_end": 0x11,
            "return": 0xFF,
            "get_time": 0x20,
            "read_file": 0x21,
            "file_exists": 0x22,
            "list_dir": 0x23,
            "random_number": 0x24,
            "write_file": 0x30,
            "append_file": 0x31,
            "log_event": 0x32,
            "notify": 0x33,
            "delete_file": 0x34,
            "create_directory": 0x35
        }
    
    def compile_sequence(self, sqvgr):
        """Компилирует SqVGr в байт-код"""
        bytecode = bytearray()
        metadata = {
            "steps": len(sqvgr["sequence"]),
            "actions": [],
            "hash": None
        }
        
        for step in sqvgr["sequence"]:
            action = step["action"]
            opcode = self.opcodes.get(action, 0x00)
            bytecode.append(opcode)
            metadata["actions"].append(action)
            
            # Добавляем параметры в зависимости от действия
            if action == "init_counter":
                # target как байт, value как int
                target_hash = hashlib.md5(step["target"].encode()).digest()[0]
                bytecode.append(target_hash)
                bytecode.extend(step["value"].to_bytes(4, 'little'))
            elif action == "console_output":
                value = step["value"].encode('utf-8')
                bytecode.append(len(value))
                bytecode.extend(value)
            elif action == "increment":
                target_hash = hashlib.md5(step["target"].encode()).digest()[0]
                bytecode.append(target_hash)
                bytecode.append(step["by"])
            elif action == "loop_start":
                condition = step["condition"]
                # Парсим условие
                parts = condition.split()
                var_hash = hashlib.md5(parts[0].encode()).digest()[0]
                limit = int(parts[2])
                bytecode.append(var_hash)
                bytecode.extend(limit.to_bytes(4, 'little'))
            elif action in ["read_file", "file_exists", "delete_file", "create_directory"]:
                path = step.get("path", "").encode('utf-8')
                bytecode.append(len(path))
                bytecode.extend(path)
            elif action in ["write_file", "append_file"]:
                path = step.get("path", "").encode('utf-8')
                content = step.get("content", "").encode('utf-8')
                bytecode.append(len(path))
                bytecode.extend(path)
                bytecode.append(len(content))
                bytecode.extend(content)
            elif action == "random_number":
                min_val = step.get("min", 0)
                max_val = step.get("max", 100)
                bytecode.extend(min_val.to_bytes(4, 'little'))
                bytecode.extend(max_val.to_bytes(4, 'little'))
        
        metadata["hash"] = hashlib.sha256(bytecode).hexdigest()[:16]
        return bytes(bytecode), metadata
    
    def disassemble(self, bytecode):
        """Дизассемблирует байт-код для отладки"""
        instructions = []
        i = 0
        reverse_opcodes = {v: k for k, v in self.opcodes.items()}
        
        while i < len(bytecode):
            op = bytecode[i]
            action = reverse_opcodes.get(op, "unknown")
            instr = {"offset": i, "op": op, "action": action}
            i += 1
            
            if action == "init_counter":
                target = bytecode[i]
                value = int.from_bytes(bytecode[i+1:i+5], 'little')
                instr["target_hash"] = target
                instr["value"] = value
                i += 5
            elif action == "console_output":
                length = bytecode[i]
                value = bytecode[i+1:i+1+length].decode('utf-8')
                instr["value"] = value
                i += 1 + length
            elif action == "increment":
                target = bytecode[i]
                by = bytecode[i+1]
                instr["target_hash"] = target
                instr["by"] = by
                i += 2
            elif action == "loop_start":
                var_hash = bytecode[i]
                limit = int.from_bytes(bytecode[i+1:i+5], 'little')
                instr["var_hash"] = var_hash
                instr["limit"] = limit
                i += 5
            elif action in ["read_file", "file_exists", "delete_file", "create_directory"]:
                length = bytecode[i]
                path = bytecode[i+1:i+1+length].decode('utf-8')
                instr["path"] = path
                i += 1 + length
            elif action in ["write_file", "append_file"]:
                path_len = bytecode[i]
                path = bytecode[i+1:i+1+path_len].decode('utf-8')
                i += 1 + path_len
                content_len = bytecode[i]
                content = bytecode[i+1:i+1+content_len].decode('utf-8')
                instr["path"] = path
                instr["content"] = content
                i += 1 + content_len
            elif action == "random_number":
                min_val = int.from_bytes(bytecode[i:i+4], 'little')
                max_val = int.from_bytes(bytecode[i+4:i+8], 'little')
                instr["min"] = min_val
                instr["max"] = max_val
                i += 8
            
            instructions.append(instr)
        
        return instructions

_compiler = BytecodeCompiler()

def compile_sequence(sqvgr):
    return _compiler.compile_sequence(sqvgr)

def disassemble(bytecode):
    return _compiler.disassemble(bytecode)