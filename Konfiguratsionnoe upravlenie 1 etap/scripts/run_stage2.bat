@echo off
REM Скрипт реальной ОС (Windows) для тестирования Этапа 2.

cd /d "%~dp0.."

echo === Тест 1: запуск без параметров ===
start /B python src\main.py
timeout /t 2 >nul
taskkill /F /IM python.exe >nul 2>&1

echo.
echo === Тест 2: запуск с параметром --vfs ===
start /B python src\main.py --vfs .\vfs_data
timeout /t 2 >nul
taskkill /F /IM python.exe >nul 2>&1

echo.
echo === Тест 3: запуск с параметром --script ===
start /B python src\main.py --script .\scripts\start_script.txt
timeout /t 3 >nul
taskkill /F /IM python.exe >nul 2>&1

echo.
echo === Тест 4: запуск с обоими параметрами ===
start /B python src\main.py --vfs .\vfs_data --script .\scripts\start_script.txt
timeout /t 3 >nul
taskkill /F /IM python.exe >nul 2>&1

echo.
echo === Тест 5: запуск с краткими формами -v и -s ===
start /B python src\main.py -v .\vfs_data -s .\scripts\start_script.txt
timeout /t 3 >nul
taskkill /F /IM python.exe >nul 2>&1

echo.
echo === Тест 6: запуск с несуществующим стартовым скриптом ===
start /B python src\main.py --script .\scripts\nonexistent.txt
timeout /t 2 >nul
taskkill /F /IM python.exe >nul 2>&1

echo.
echo Все тесты завершены.
pause
