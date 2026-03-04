from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Jarvis Test Server</h1><p>Flask работает! Порт 8888</p>'

if __name__ == '__main__':
    print('=' * 50)
    print('Тестовый сервер запущен')
    print('=' * 50)
    print('Открой в браузере: http://localhost:8888')
    print('Нажми Ctrl+C для остановки')
    print('=' * 50)
    app.run(host='0.0.0.0', port=8888, debug=True)
