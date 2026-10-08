"""Эмулятор командной оболочки UNIX-подобной ОС.

Практическая работа №1 по дисциплине «Конфигурационное управление».
Вариант №15, группа ИКБО-50-25, РТУ МИРЭА — 2026.

Этап 1. REPL — минимальный прототип с GUI-интерфейсом.
Этап 2. Конфигурация — параметры командной строки и стартовый скрипт.
"""

from tkinter import *
from tkinter import ttk
from getpass import getuser
from socket import gethostname
import sys
import os

"""Глобальные параметры конфигурации (Этап 2)"""

VFS_PATH = None
START_SCRIPT = None



"""Разбор аргументов командной строки (Этап 2)"""

def parse_argv():
    """Разбирает аргументы командной строки.

    Поддерживаются параметры:
      --vfs,   -v  — путь к физическому расположению VFS;
      --script,-s  — путь к стартовому скрипту.
    """
    global VFS_PATH, START_SCRIPT
    argv = sys.argv[1:]
    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("--vfs", "-v") and i + 1 < len(argv):
            VFS_PATH = argv[i + 1]
            i += 2
        elif arg in ("--script", "-s") and i + 1 < len(argv):
            START_SCRIPT = argv[i + 1]
            i += 2
        else:
            i += 1

"""Парсер команд (Этап 1)"""

def parse(raw):
    """Разбирает строку на команду и аргументы.

    Поддерживает одинарные и двойные кавычки.
    Возвращает (cmd, args) или ('__error__', [сообщение]).
    """
    raw = raw.strip()
    if not raw:
        return None, []

    tokens = []
    buf = ""
    quote = None
    in_token = False

    for ch in raw:
        if quote:
            if ch == quote:
                quote = None
            else:
                buf += ch
            in_token = True
        elif ch in ("'", '"'):
            quote = ch
            in_token = True
        elif ch == " " or ch == "\t":
            if in_token:
                tokens.append(buf)
                buf = ""
                in_token = False
        else:
            buf += ch
            in_token = True

    if quote is not None:
        return "__error__", ["незакрытая кавычка"]
    if in_token:
        tokens.append(buf)

    if not tokens:
        return None, []
    return tokens[0], tokens[1:]

"""
# Команды-заглушки (Этап 1)
"""

def cmd_ls(args):
    """Заглушка ls: выводит имя команды и её аргументы."""
    return f"ls: {args}"


def cmd_cd(args):
    """Заглушка cd: выводит имя команды и её аргументы."""
    return f"cd: {args}"

"""Диспетчер команд"""

def execute(raw):
    """разбирает ввод и вызывает нужную команду."""
    cmd, args = parse(raw)

    if cmd is None:
        return ""
    if cmd == "__error__":
        return f"Ошибка парсинга: {args[0]}"

    if cmd == "exit":
        window.destroy()
        return ""

    if cmd == "ls":
        return cmd_ls(args)
    if cmd == "cd":
        return cmd_cd(args)

    return f"Ошибка: неизвестная команда '{cmd}'"


"""Выполнение стартового скрипта (Этап 2)"""

def run_script(path):
    """Выполняет стартовый скрипт.

    Поддерживает комментарии (строки, начинающиеся с '#').
    При выполнении на экране отображается как ввод, так и вывод,
    имитируя диалог с пользователем.
    Сообщает об ошибках чтения и выполнения скрипта.
    """
    if not os.path.isfile(path):
        result["text"] = f"Ошибка: стартовый скрипт не найден: {path}"
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError as e:
        result["text"] = f"Ошибка чтения скрипта: {e}"
        return

    for line in lines:
        line = line.rstrip("\n")
        stripped = line.strip()

        """Пропускаем пустые строки и комментарии"""
        if not stripped or stripped.startswith("#"):
            continue

        out = execute(stripped)

        """Если окно закрылось (exit) — выходим"""
        if out == "" and not window.winfo_exists():
            return

        """Имитация диалога: ввод + вывод"""
        block = f"> {stripped}\n{out}" if out else f"> {stripped}"
        story["text"] = block + "\n" + story["text"]

        if out:
            result["text"] = out


"""Отладочный вывод параметров (Этап 2)"""

def dump_params():
    """Отладочный вывод всех заданных параметров при запуске эмулятора."""
    lines = [
        "=== Параметры эмулятора ===",
        f"VFS path:     {VFS_PATH if VFS_PATH else '(не задан)'}",
        f"Start script: {START_SCRIPT if START_SCRIPT else '(не задан)'}",
    ]
    text = "\n".join(lines)
    story["text"] = text + "\n\n" + story["text"]


"""Обработчик ввода пользователя"""

def go(event=None):
    """Обработчик нажатия кнопки Go / клавиши Enter."""
    raw = entry.get()
    if not raw.strip():
        return

    out = execute(raw)
    if out == "" and not window.winfo_exists():
        return

    """Имитация диалога: ввод + вывод"""
    block = f"> {raw}\n{out}" if out else f"> {raw}"
    story["text"] = block + "\n" + story["text"]

    if out:
        result["text"] = out
    entry.delete(0, END)

"""Инициализация GUI"""

parse_argv()

window = Tk()
window.title(f"Эмулятор - [{getuser()}@{gethostname()}]")
window.geometry("1000x500")
window.configure(bg='black')

entry = ttk.Entry(window)
entry.pack()
entry.bind("<Return>", go)

com_go = Button(window, text="Go", bg="green3",
                font=("Arial", 15, "normal"), command=go)

story = Label(window, text="", font=("Arial", 15, "normal"),
              justify=LEFT, anchor="nw", bg='black', fg='white')
story_t = Label(window, text="История:", font=("Arial", 15, "normal"),
                bg='black', fg='white')
result = Label(window, text="", font=("Arial", 10, "normal"),
               bg='black', fg='white', justify=LEFT, anchor="w")

entry.place(x=450, y=200)
com_go.place(x=580, y=200)
result.place(x=500, y=240)
story.place(x=100, y=100, width=800, height=90)
story_t.place(x=100, y=80)

"""Отладочный вывод параметров при запуске (требование цели Этапа 2)"""
dump_params()

"""Выполнение стартового скрипта, если он задан"""
if START_SCRIPT:
    run_script(START_SCRIPT)

window.mainloop()
