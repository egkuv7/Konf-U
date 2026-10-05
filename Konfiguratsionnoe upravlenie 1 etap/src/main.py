"""Эмулятор командной оболочки UNIX-подобной ОС.

Практическая работа №1 по дисциплине «Конфигурационное управление».
Вариант №15, группа ИКБО-50-25, РТУ МИРЭА — 2026.

Этап 1. REPL — минимальный прототип с GUI-интерфейсом.
"""

from tkinter import *
from tkinter import ttk
from getpass import getuser
from socket import gethostname


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


def cmd_ls(args):
    """Заглушка ls: выводит имя команды и её аргументы."""
    return f"ls: {args}"


def cmd_cd(args):
    """Заглушка cd: выводит имя команды и её аргументы."""
    return f"cd: {args}"


def execute(raw):
    """Диспетчер команд: разбирает ввод и вызывает нужную команду."""
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


def go(event=None):
    """Обработчик нажатия кнопки Go / клавиши Enter."""
    raw = entry.get()
    if not raw.strip():
        return

    out = execute(raw)
    if out == "" and not window.winfo_exists():
        return

    # Имитация диалога: ввод + вывод
    block = f"> {raw}\n{out}" if out else f"> {raw}"
    story["text"] = block + "\n" + story["text"]

    if out:
        result["text"] = out
    entry.delete(0, END)

window = Tk()
window.title(f"Эмулятор - [{getuser()}@{gethostname()}]")
window.geometry("1000x500")
window.configure(bg='black')

entry = ttk.Entry(window)
entry.pack()
entry.bind("<Return>", go)   # Enter = выполнить команду

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

story["text"] = (
    "> ls /home\nls: ['/home']\n"
    "> cd \"my dir\"\ncd: ['my dir']\n"
    "> unknown\nОшибка: неизвестная команда 'unknown'\n"
    "> ls 'a b' c\nls: ['a b', 'c']\n"
)

window.mainloop()
