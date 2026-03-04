# Jarvis 3.0.1 - Complete Meta-Engine Platform

[![CI](https://github.com/Khushvakht799/jarvis-45platform/actions/workflows/ci.yml/badge.svg)](https://github.com/Khushvakht799/jarvis-45platform/actions/workflows/ci.yml)
[![Release](https://github.com/Khushvakht799/jarvis-45platform/actions/workflows/release.yml/badge.svg)](https://github.com/Khushvakht799/jarvis-45platform/actions/workflows/release.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📋 Описание

Jarvis — это мета-движок с 10-уровневой архитектурой и поддержкой векторных графов (VGr). Проект реализует полный цикл обработки команд: понимание → действие → контроль → эволюция.

## 🚀 Быстрый старт

### Установка

```bash
# Клонирование репозитория
git clone https://github.com/Khushvakht799/jarvis-45platform.git
cd jarvis-45platform

# Создание виртуального окружения (рекомендуется)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Установка зависимостей
pip install -r requirements.txt
```

### Запуск

**Веб-интерфейс:**
```bash
python run_web.py
```
Откройте браузер: http://localhost:8080

**Демон (фоновый режим):**
```bash
python run_daemon.py --sync --autonomous
```

**Сетевой сервер:**
```bash
python run_server.py
```

### Тестирование

```bash
# Запуск всех тестов
pytest tests/ -v

# С покрытием кода
pytest tests/ --cov=core --cov-report=html
```

## 🏗 Архитектура

### 10 уровней платформы

1. **Логический** - правила в интерпретаторе
2. **Структурный** - узлы в JVGr/AVGr
3. **Языковой** - операторы в SqVGr
4. **Модульный** - пакеты в core
5. **Алгоритмический** - рекурсия
6. **Технологический** - Flask, requests
7. **Организационный** - демоны
8. **Данные** - JSON/YAML
9. **Интерпретация** - компилятор
10. **Управление** - оркестраторы

### Основные VGr форматы

| Формат | Описание |
|--------|----------|
| JVGr | Семантический граф в JSON |
| AVGr | Вектор действия (intent) |
| BVGr | Бинарное состояние |
| SqVGr | Последовательность действий |
| GiVGr | Суть выполнения |
| SyVGr | Анализ симптомов |
| PVGr | Физический уровень |
| LIVGr | Жизненный цикл |

## 📁 Структура проекта

```
jarvis-45platform/
├── core/               # Ядро системы
│   ├── framework/      # Базовый ввод/вывод
│   ├── engine/         # Интерпретатор, JIT
│   ├── orchestrator/   # Оркестрация
│   ├── daemon/         # Демоны
│   ├── metacontrol/    # Память, эволюция
│   ├── network/        # Сеть, discovery
│   ├── physics/        # Сенсоры, актуаторы
│   ├── life/           # Автономия
│   └── compiler/       # Компилятор
├── web/                # Веб-интерфейс
│   ├── templates/      # HTML шаблоны
│   └── static/         # CSS, JS
├── tests/              # Тесты
├── .github/            # GitHub Actions
├── run_*.py            # Точки входа
└── requirements.txt    # Зависимости
```

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `JARVIS_HOST` | Хост для сервера | `0.0.0.0` |
| `JARVIS_PORT` | Порт для сервера | `5000` |
| `JARVIS_DEBUG` | Режим отладки | `False` |

### Флаги запуска

```bash
python run_daemon.py --sync      # Включить сетевую синхронизацию
python run_daemon.py --autonomous # Автономный режим
python run_daemon.py --distributed # Распределённый режим
python run_daemon.py --no-cache   # Отключить кэш компилятора
```

## 🧪 Примеры команд

```bash
# Базовые команды
скажи привет три раза
сколько времени
случайное число

# Работа с файлами
запиши в файл test.txt привет мир
прочитай файл test.txt

# Распределённое выполнение
dist:сколько времени
```

## 🤝 Участие в разработке

1. Форкните репозиторий
2. Создайте ветку (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

### Требования к PR
- Добавляйте тесты для новой функциональности
- Убедитесь, что все тесты проходят
- Следуйте стилю кода (flake8)

## 📄 Лицензия

MIT License — подробности в файле [LICENSE](LICENSE)

## 📊 Статус проекта

![MVP](https://img.shields.io/badge/status-MVP-yellow)
![Version](https://img.shields.io/badge/version-3.0.1-blue)
![Tests](https://img.shields.io/badge/tests-42%20passing-brightgreen)

## 🙏 Благодарности

Всем, кто участвовал в проектировании 10-уровневой архитектуры и разработке векторных форматов VGr.