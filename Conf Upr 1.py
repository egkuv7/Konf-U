
#Этап 1
"""from tkinter import *
from tkinter import ttk
from getpass import getuser
from socket import gethostname

def parse(raw):
    
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
    return f"ls: {args}"


def cmd_cd(args):
    return f"cd: {args}"


def execute(raw):
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
    raw = entry.get()
    if not raw.strip():
        return

    out = execute(raw)
    if out == "" and not window.winfo_exists():
        return

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

story["text"] = (
    "> ls /home\nls: ['/home']\n"
    "> cd \"my dir\"\ncd: ['my dir']\n"
    "> unknown\nОшибка: неизвестная команда 'unknown'\n"
    "> ls 'a b' c\nls: ['a b', 'c']\n"
)

window.mainloop()
"""
#||||||||||||||||||||||||||||||||||||||| Этап 2
"""
from tkinter import *
from tkinter import ttk
from getpass import getuser
from socket import gethostname
import sys
import os

VFS_PATH = None
START_SCRIPT = None


def parse_argv():
    
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

def parse(raw):
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
    return f"ls: {args}"


def cmd_cd(args):
    return f"cd: {args}"


def execute(raw):
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



def run_script(path):
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

        # Пропускаем пустые строки и комментарии
        if not stripped or stripped.startswith("#"):
            continue

        out = execute(stripped)

        # Если окно закрылось (exit) — выходим
        if out == "" and not window.winfo_exists():
            return

        # Имитация диалога: ввод + вывод
        block = f"> {stripped}\n{out}" if out else f"> {stripped}"
        story["text"] = block + "\n" + story["text"]

        if out:
            result["text"] = out



def go(event=None):
    raw = entry.get()
    if not raw.strip():
        return

    out = execute(raw)
    if out == "" and not window.winfo_exists():
        return

    block = f"> {raw}\n{out}" if out else f"> {raw}"
    story["text"] = block + "\n" + story["text"]

    if out:
        result["text"] = out
    entry.delete(0, END)


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



def dump_params():
    
    lines = [
        "=== Параметры эмулятора ===",
        f"VFS path:     {VFS_PATH if VFS_PATH else '(не задан)'}",
        f"Start script: {START_SCRIPT if START_SCRIPT else '(не задан)'}",
    ]
    text = "\n".join(lines)
    story["text"] = text + "\n\n" + story["text"]


dump_params()



if START_SCRIPT:
    run_script(START_SCRIPT)


window.mainloop()"""

"""
|||||||||||||||||||||||||||||||||||||| Этап 3

from tkinter import *
from tkinter import ttk
from getpass import getuser
from socket import gethostname
import sys
import os
import base64
import hashlib
import xml.etree.ElementTree as ET



VFS_PATH = None
START_SCRIPT = None


def parse_argv():
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



class VFSNode:
    def __init__(self, name, is_dir=False, content=""):
        self.name = name
        self.is_dir = is_dir
        self.content = content          # текст или base64 (для бинарных)
        self.children = {}              # имя -> VFSNode

    def add(self, child):
        self.children[child.name] = child

    def find(self, name):
        return self.children.get(name)


class VFS:
    
    def __init__(self, name="vfs"):
        self.name = name
        self.root = VFSNode("/", is_dir=True)
        self.cwd = self.root
        self.source_hash = ""

    def load_xml(self, path):
       
        if not os.path.isfile(path):
            return f"Ошибка: файл VFS не найден: {path}"
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except ET.ParseError as e:
            return f"Ошибка: неверный формат XML ({e})"
        except OSError as e:
            return f"Ошибка чтения файла VFS: {e}"

        self.name = root.get("name", "vfs")
        self.root = VFSNode("/", is_dir=True)

        def build(xml_node, parent):
            for child in xml_node:
                is_dir = (child.tag == "dir")
                name = child.get("name", "")
                if not name:
                    return "Ошибка: узел без атрибута name"

                if is_dir:
                    new = VFSNode(name, is_dir=True)
                    err = build(child, new)
                    if err:
                        return err
                else:
                    data = child.text or ""
                    encoding = child.get("encoding", "text")
                    if encoding == "base64":
                        try:
                            base64.b64decode(data, validate=True)
                        except Exception:
                            return f"Ошибка: некорректный base64 в '{name}'"
                    new = VFSNode(name, is_dir=False, content=data)
                parent.add(new)
            return None

        err = build(root, self.root)
        if err:
            return err

        # SHA-256 от исходных данных файла
        try:
            with open(path, "rb") as f:
                self.source_hash = hashlib.sha256(f.read()).hexdigest()
        except OSError as e:
            return f"Ошибка чтения файла VFS: {e}"

        return None

    def info(self):
        
        return (f"VFS name: {self.name}\n"
                f"SHA-256:  {self.source_hash}")



def parse(raw):
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
    return f"ls: {args}"


def cmd_cd(args):
    return f"cd: {args}"



def execute(raw):
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
    if cmd == "vfs-info":            # <-- Этап 3
        return vfs.info()

    return f"Ошибка: неизвестная команда '{cmd}'"


def run_script(path):
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

        if not stripped or stripped.startswith("#"):
            continue

        out = execute(stripped)

        if out == "" and not window.winfo_exists():
            return

        block = f"> {stripped}\n{out}" if out else f"> {stripped}"
        story["text"] = block + "\n" + story["text"]

        if out:
            result["text"] = out


def go(event=None):
    raw = entry.get()
    if not raw.strip():
        return

    out = execute(raw)
    if out == "" and not window.winfo_exists():
        return

    block = f"> {raw}\n{out}" if out else f"> {raw}"
    story["text"] = block + "\n" + story["text"]

    if out:
        result["text"] = out
    entry.delete(0, END)


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


vfs = VFS()
vfs_error = None
if VFS_PATH:
    vfs_error = vfs.load_xml(VFS_PATH)



def dump_params():
    lines = [
        "=== Параметры эмулятора ===",
        f"VFS path:     {VFS_PATH if VFS_PATH else '(не задан)'}",
        f"Start script: {START_SCRIPT if START_SCRIPT else '(не задан)'}",
        f"VFS name:     {vfs.name}",
        f"VFS SHA-256:  {vfs.source_hash if vfs.source_hash else '(нет)'}",
    ]
    story["text"] = "\n".join(lines) + "\n\n" + story["text"]


dump_params()


if vfs_error:
    result["text"] = vfs_error
    story["text"] = vfs_error + "\n" + story["text"]



if START_SCRIPT:
    run_script(START_SCRIPT)


window.mainloop()"""

"""
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||| Этап 4

from tkinter import *
from tkinter import ttk
from getpass import getuser
from socket import gethostname
import sys
import os
import base64
import hashlib
import xml.etree.ElementTree as ET



VFS_PATH = None
START_SCRIPT = None


def parse_argv():
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


class VFSNode:
    def __init__(self, name, is_dir=False, content="", owner="user"):
        self.name = name
        self.is_dir = is_dir
        self.content = content          # текст или base64
        self.owner = owner
        self.children = {}

    def add(self, child):
        self.children[child.name] = child

    def find(self, name):
        return self.children.get(name)


class VFS:
    def __init__(self, name="vfs"):
        self.name = name
        self.root = VFSNode("/", is_dir=True, owner="root")
        self.cwd = self.root
        self.source_hash = ""

    def load_xml(self, path):
        if not os.path.isfile(path):
            return f"Ошибка: файл VFS не найден: {path}"
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except ET.ParseError as e:
            return f"Ошибка: неверный формат XML ({e})"
        except OSError as e:
            return f"Ошибка чтения файла VFS: {e}"

        self.name = root.get("name", "vfs")
        self.root = VFSNode("/", is_dir=True, owner="root")

        def build(xml_node, parent):
            for child in xml_node:
                is_dir = (child.tag == "dir")
                name = child.get("name", "")
                if not name:
                    return "Ошибка: узел без атрибута name"
                owner = child.get("owner", "user")
                if is_dir:
                    new = VFSNode(name, is_dir=True, owner=owner)
                    err = build(child, new)
                    if err:
                        return err
                else:
                    data = child.text or ""
                    encoding = child.get("encoding", "text")
                    if encoding == "base64":
                        try:
                            base64.b64decode(data, validate=True)
                        except Exception:
                            return f"Ошибка: некорректный base64 в '{name}'"
                    new = VFSNode(name, is_dir=False, content=data, owner=owner)
                parent.add(new)
            return None

        err = build(root, self.root)
        if err:
            return err

        try:
            with open(path, "rb") as f:
                self.source_hash = hashlib.sha256(f.read()).hexdigest()
        except OSError as e:
            return f"Ошибка чтения файла VFS: {e}"
        return None

    def info(self):
        return (f"VFS name: {self.name}\n"
                f"SHA-256:  {self.source_hash}")


    def resolve(self, path):
       
        if not path:
            return self.cwd
        cur = self.root if path.startswith("/") else self.cwd
        parts = [p for p in path.split("/") if p and p != "."]
        for p in parts:
            if p == "..":
                continue   # упрощённая обработка (без родителя)
            if not cur.is_dir:
                return None
            cur = cur.find(p)
            if cur is None:
                return None
        return cur


    def resolve_parent(self, path):
        
        if not path or path == "/":
            return None, None
        if path.startswith("/"):
            parent_path = "/".join(path.split("/")[:-1]) or "/"
        else:
            parent_path = "/".join(path.split("/")[:-1]) or "."
        last = path.split("/")[-1]
        parent = self.resolve(parent_path) if parent_path not in (".", "") else self.cwd
        return parent, last



def parse(raw):
    raw = raw.strip()
    if not raw:
        return None, []

    tokens, buf, quote, in_token = [], "", None, False
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
                buf, in_token = "", False
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
    
    if len(args) > 1:
        return "ls: неверное число аргументов"

    path = args[0] if args else None
    node = vfs.resolve(path) if path else vfs.cwd
    if node is None:
        return f"ls: {path}: нет такого файла или каталога"

    if not node.is_dir:
        return node.name

    if not node.children:
        return ""      # пустой каталог

    lines = []
    for name in sorted(node.children):
        child = node.children[name]
        lines.append(name + ("/" if child.is_dir else ""))
    return "\n".join(lines)


def cmd_cd(args):
   
    if len(args) != 1:
        return "cd: неверное число аргументов"

    target = vfs.resolve(args[0])
    if target is None:
        return f"cd: {args[0]}: нет такого каталога"
    if not target.is_dir:
        return f"cd: {args[0]}: не каталог"

    vfs.cwd = target
    return ""


def cmd_who(args):
   
    if args:
        return "who: не принимает аргументов"

    users = set()
    def walk(node):
        if not node.is_dir:
            users.add(node.owner)
        for c in node.children.values():
            walk(c)
    walk(vfs.root)

    if not users:
        users.add("user")
    return "\n".join(sorted(users))


def cmd_cat(args):
    
    if not args:
        return "cat: не указан файл"

    outputs = []
    for path in args:
        node = vfs.resolve(path)
        if node is None:
            outputs.append(f"cat: {path}: нет такого файла")
        elif node.is_dir:
            outputs.append(f"cat: {path}: это каталог")
        else:
            outputs.append(node.content)
    return "\n".join(outputs)



def execute(raw):
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
    if cmd == "who":
        return cmd_who(args)
    if cmd == "cat":
        return cmd_cat(args)
    if cmd == "vfs-info":
        return vfs.info()

    return f"Ошибка: неизвестная команда '{cmd}'"



def run_script(path):
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
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        out = execute(stripped)
        if out == "" and not window.winfo_exists():
            return
        block = f"> {stripped}\n{out}" if out else f"> {stripped}"
        story["text"] = block + "\n" + story["text"]
        if out:
            result["text"] = out



def go(event=None):
    raw = entry.get()
    if not raw.strip():
        return
    out = execute(raw)
    if out == "" and not window.winfo_exists():
        return
    block = f"> {raw}\n{out}" if out else f"> {raw}"
    story["text"] = block + "\n" + story["text"]
    if out:
        result["text"] = out
    entry.delete(0, END)



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



vfs = VFS()
vfs_error = None
if VFS_PATH:
    vfs_error = vfs.load_xml(VFS_PATH)



def dump_params():
    lines = [
        "=== Параметры эмулятора ===",
        f"VFS path:     {VFS_PATH if VFS_PATH else '(не задан)'}",
        f"Start script: {START_SCRIPT if START_SCRIPT else '(не задан)'}",
        f"VFS name:     {vfs.name}",
        f"VFS SHA-256:  {vfs.source_hash if vfs.source_hash else '(нет)'}",
    ]
    story["text"] = "\n".join(lines) + "\n\n" + story["text"]


dump_params()

if vfs_error:
    result["text"] = vfs_error
    story["text"] = vfs_error + "\n" + story["text"]



if START_SCRIPT:
    run_script(START_SCRIPT)


window.mainloop()"""

from tkinter import *
from tkinter import ttk
from getpass import getuser
from socket import gethostname
import sys
import os
import base64
import hashlib
import xml.etree.ElementTree as ET



VFS_PATH = None
START_SCRIPT = None


def parse_argv():
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



class VFSNode:
    def __init__(self, name, is_dir=False, content="", owner="user"):
        self.name = name
        self.is_dir = is_dir
        self.content = content          # текст или base64
        self.owner = owner
        self.children = {}

    def add(self, child):
        self.children[child.name] = child

    def find(self, name):
        return self.children.get(name)


class VFS:
    def __init__(self, name="vfs"):
        self.name = name
        self.root = VFSNode("/", is_dir=True, owner="root")
        self.cwd = self.root
        self.source_hash = ""

    def load_xml(self, path):
        if not os.path.isfile(path):
            return f"Ошибка: файл VFS не найден: {path}"
        try:
            tree = ET.parse(path)
            root = tree.getroot()
        except ET.ParseError as e:
            return f"Ошибка: неверный формат XML ({e})"
        except OSError as e:
            return f"Ошибка чтения файла VFS: {e}"

        self.name = root.get("name", "vfs")
        self.root = VFSNode("/", is_dir=True, owner="root")

        def build(xml_node, parent):
            for child in xml_node:
                is_dir = (child.tag == "dir")
                name = child.get("name", "")
                if not name:
                    return "Ошибка: узел без атрибута name"
                owner = child.get("owner", "user")
                if is_dir:
                    new = VFSNode(name, is_dir=True, owner=owner)
                    err = build(child, new)
                    if err:
                        return err
                else:
                    data = child.text or ""
                    encoding = child.get("encoding", "text")
                    if encoding == "base64":
                        try:
                            base64.b64decode(data, validate=True)
                        except Exception:
                            return f"Ошибка: некорректный base64 в '{name}'"
                    new = VFSNode(name, is_dir=False, content=data, owner=owner)
                parent.add(new)
            return None

        err = build(root, self.root)
        if err:
            return err

        try:
            with open(path, "rb") as f:
                self.source_hash = hashlib.sha256(f.read()).hexdigest()
        except OSError as e:
            return f"Ошибка чтения файла VFS: {e}"
        return None

    def info(self):
        return (f"VFS name: {self.name}\n"
                f"SHA-256:  {self.source_hash}")


    def resolve(self, path):
        if not path:
            return self.cwd
        cur = self.root if path.startswith("/") else self.cwd
        parts = [p for p in path.split("/") if p and p != "."]
        for p in parts:
            if p == "..":
                continue
            if not cur.is_dir:
                return None
            cur = cur.find(p)
            if cur is None:
                return None
        return cur

    def resolve_parent(self, path):
        if not path or path == "/":
            return None, None

        parts = [p for p in path.split("/") if p and p != "."]
        if not parts:
            return None, None

        last = parts[-1]
        if path.startswith("/"):
            parent_path = "/" + "/".join(parts[:-1])
        else:
            parent_path = "/".join(parts[:-1]) if len(parts) > 1 else "."

        parent = self.cwd if parent_path in (".", "") else self.resolve(parent_path)
        return parent, last



def parse(raw):
    raw = raw.strip()
    if not raw:
        return None, []

    tokens, buf, quote, in_token = [], "", None, False
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
                buf, in_token = "", False
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
    if len(args) > 1:
        return "ls: неверное число аргументов"
    path = args[0] if args else None
    node = vfs.resolve(path) if path else vfs.cwd
    if node is None:
        return f"ls: {path}: нет такого файла или каталога"
    if not node.is_dir:
        return node.name
    if not node.children:
        return ""
    lines = []
    for name in sorted(node.children):
        child = node.children[name]
        lines.append(name + ("/" if child.is_dir else ""))
    return "\n".join(lines)


def cmd_cd(args):
    if len(args) != 1:
        return "cd: неверное число аргументов"
    target = vfs.resolve(args[0])
    if target is None:
        return f"cd: {args[0]}: нет такого каталога"
    if not target.is_dir:
        return f"cd: {args[0]}: не каталог"
    vfs.cwd = target
    return ""


def cmd_who(args):
    if args:
        return "who: не принимает аргументов"
    users = set()
    def walk(node):
        if not node.is_dir:
            users.add(node.owner)
        for c in node.children.values():
            walk(c)
    walk(vfs.root)
    if not users:
        users.add("user")
    return "\n".join(sorted(users))


def cmd_cat(args):
    if not args:
        return "cat: не указан файл"
    outputs = []
    for path in args:
        node = vfs.resolve(path)
        if node is None:
            outputs.append(f"cat: {path}: нет такого файла")
        elif node.is_dir:
            outputs.append(f"cat: {path}: это каталог")
        else:
            outputs.append(node.content)
    return "\n".join(outputs)


def cmd_mkdir(args):
    if len(args) != 1:
        return "mkdir: неверное число аргументов"

    path = args[0]
    parent, name = vfs.resolve_parent(path)
    if parent is None:
        return f"mkdir: {path}: неверный путь"
    if not parent.is_dir:
        return f"mkdir: {path}: родитель не каталог"
    if parent.find(name) is not None:
        return f"mkdir: {path}: уже существует"

    parent.add(VFSNode(name, is_dir=True, owner=parent.owner))
    return ""


def cmd_mv(args):
    if len(args) != 2:
        return "mv: неверное число аргументов"

    src_path, dst_path = args

    src = vfs.resolve(src_path)
    if src is None:
        return f"mv: {src_path}: нет такого файла или каталога"

    
    if src is vfs.root:
        return "mv: нельзя переместить корень"

    dst_node = vfs.resolve(dst_path)
    if dst_node is src:
        return f"mv: {dst_path}: нельзя переместить в самого себя"
    if dst_node is not None and dst_node.is_dir:
        new_parent = dst_node
        new_name = src.name
    else:
        new_parent, new_name = vfs.resolve_parent(dst_path)
        if new_parent is None:
            return f"mv: {dst_path}: неверный путь назначения"
        if not new_parent.is_dir:
            return f"mv: {dst_path}: родитель не каталог"

    if new_parent.find(new_name) is not None:
        return f"mv: {dst_path}: уже существует"

    def contains(ancestor, candidate):
        if ancestor is candidate:
            return True
        if not ancestor.is_dir:
            return False
        for c in ancestor.children.values():
            if contains(c, candidate):
                return True
        return False

    if src.is_dir and contains(src, new_parent):
        return f"mv: {dst_path}: нельзя переместить каталог внутрь себя"

    # Находим старого родителя
    old_parent, _ = vfs.resolve_parent(src_path)
    if old_parent is None:
        # относительный путь без "/"
        if src.name in vfs.cwd.children:
            old_parent = vfs.cwd
        else:
            return f"mv: {src_path}: не удалось определить родителя"

    if src.name in old_parent.children:
        del old_parent.children[src.name]

    src.name = new_name
    new_parent.add(src)
    return ""



def execute(raw):
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
    if cmd == "who":
        return cmd_who(args)
    if cmd == "cat":
        return cmd_cat(args)
    if cmd == "mkdir":            # <-- Этап 5
        return cmd_mkdir(args)
    if cmd == "mv":               # <-- Этап 5
        return cmd_mv(args)
    if cmd == "vfs-info":
        return vfs.info()

    return f"Ошибка: неизвестная команда '{cmd}'"


def run_script(path):
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
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        out = execute(stripped)
        if out == "" and not window.winfo_exists():
            return
        block = f"> {stripped}\n{out}" if out else f"> {stripped}"
        story["text"] = block + "\n" + story["text"]
        if out:
            result["text"] = out


def go(event=None):
    raw = entry.get()
    if not raw.strip():
        return
    out = execute(raw)
    if out == "" and not window.winfo_exists():
        return
    block = f"> {raw}\n{out}" if out else f"> {raw}"
    story["text"] = block + "\n" + story["text"]
    if out:
        result["text"] = out
    entry.delete(0, END)

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


vfs = VFS()
vfs_error = None
if VFS_PATH:
    vfs_error = vfs.load_xml(VFS_PATH)


def dump_params():
    lines = [
        "=== Параметры эмулятора ===",
        f"VFS path:     {VFS_PATH if VFS_PATH else '(не задан)'}",
        f"Start script: {START_SCRIPT if START_SCRIPT else '(не задан)'}",
        f"VFS name:     {vfs.name}",
        f"VFS SHA-256:  {vfs.source_hash if vfs.source_hash else '(нет)'}",
    ]
    story["text"] = "\n".join(lines) + "\n\n" + story["text"]


dump_params()

if vfs_error:
    result["text"] = vfs_error
    story["text"] = vfs_error + "\n" + story["text"]


if START_SCRIPT:
    run_script(START_SCRIPT)


window.mainloop()