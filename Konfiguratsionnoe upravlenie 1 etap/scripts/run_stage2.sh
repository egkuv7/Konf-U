#!/usr/bin/env bash
"""Скрипт реальной ОС для тестирования Этапа 2.
Запускает эмулятор с параметрами командной строки.
"""
set -e

"""Переход в корень репозитория (на случай запуска из другой директории)"""
cd "$(dirname "$0")/.."

echo "=== Тест 1: запуск без параметров ==="
python3 src/main.py &
PID=$!
sleep 2
kill $PID 2>/dev/null || true

echo ""
echo "=== Тест 2: запуск с параметром --vfs ==="
python3 src/main.py --vfs ./vfs_data &
PID=$!
sleep 2
kill $PID 2>/dev/null || true

echo ""
echo "=== Тест 3: запуск с параметром --script ==="
python3 src/main.py --script ./scripts/start_script.txt &
PID=$!
sleep 3
kill $PID 2>/dev/null || true

echo ""
echo "=== Тест 4: запуск с обоими параметрами ==="
python3 src/main.py --vfs ./vfs_data --script ./scripts/start_script.txt &
PID=$!
sleep 3
kill $PID 2>/dev/null || true

echo ""
echo "=== Тест 5: запуск с краткими формами -v и -s ==="
python3 src/main.py -v ./vfs_data -s ./scripts/start_script.txt &
PID=$!
sleep 3
kill $PID 2>/dev/null || true

echo ""
echo "=== Тест 6: запуск с несуществующим стартовым скриптом ==="
python3 src/main.py --script ./scripts/nonexistent.txt &
PID=$!
sleep 2
kill $PID 2>/dev/null || true

echo ""
echo "Все тесты завершены."
