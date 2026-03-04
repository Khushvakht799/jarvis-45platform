def console_output(text):
    """Примитивный фреймворк вывода"""
    print(f"[Jarvis]: {text}")
    return {"status": "ok", "output": text}
