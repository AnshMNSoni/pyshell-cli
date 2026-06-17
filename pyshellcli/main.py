import json
import os
import random
import string
import threading
import time

import psutil
import pyfiglet
import pyperclip
from rich.console import Console
from rich.prompt import Prompt

import pyshellcli.config as config
from pyshellcli.equations import Equations
from pyshellcli.game import Game
from pyshellcli.git_commands import Git
from pyshellcli.graphs import GraphPlotter
from pyshellcli.linux_commands import Commands
from pyshellcli.song import Song
from pyshellcli.statistical import StatisticsCalculator
from pyshellcli.stocks import Stock
from pyshellcli.task import Task
from pyshellcli.terminals import Terminal
from pyshellcli.weather import Weather
from dotenv import load_dotenv
from pyshellcli.bulk_file_rename import BulkRenamer
from pyshellcli.ping import ping 
from pyshellcli.shortprompt import ShortPrompt
from pyshellcli.search import FileSearcher

load_dotenv()

console = Console()
USER_FILE = os.path.join("pyshellcli", "users.json")
lock = threading.Lock()
scheduled_jobs = {}
commands = {}
stop_scheduler = False
prompt_flag = True
prompt = ShortPrompt()

# Load users

def clipboard_copy(text):
    with lock:
        pyperclip.copy(text)
        console.print("Text copied to clipboard!", style="bold green")


def clipboard_paste():
    with lock:
        console.print(f"Clipboard Content: {pyperclip.paste()}", style="bold yellow")


# Synchronization
def list_processes(*args):
    for proc in psutil.process_iter(["pid", "name"]):
        console.print(f"{proc.info['pid']} - {proc.info['name']}")


def kill_process(args):
    if not args:
        console.print("Usage: kill <PID>", style="bold red")
        return
    try:
        psutil.Process(int(args[0])).terminate()
        console.print(f"Process {args[0]} terminated", style="bold red")
    except Exception as e:
        console.print(str(e), style="bold red")


def generate_password(*args):
    length = Prompt.ask("Enter password length (default 12)", default="12")
    try:
        length = int(length)
    except ValueError:
        console.print("Invalid input. Using default length (12)", style="bold red")
        length = 12
        display_prompt()
        return

    characters = string.ascii_letters + string.digits + string.punctuation
    password = "".join(random.choice(characters) for _ in range(length))
    console.print(f"Generated Password: {password}", style="bold green")
    clipboard_copy(password)


# changing and displaying terminal
terminal = Terminal()


def display_prompt():
    if config.current_terminal_layout == 1:
        Terminal().terminal_1()
    elif config.current_terminal_layout == 2:
        Terminal().terminal_2()
    elif config.current_terminal_layout == 3:
        Terminal().terminal_3()
    elif config.current_terminal_layout == 4:
        Terminal().terminal_4()
    elif config.current_terminal_layout == 5:
        Terminal().terminal_5()
    elif config.current_terminal_layout == 6:
        Terminal().terminal_6()
    elif config.current_terminal_layout == 7:
        Terminal().terminal_7()
    elif config.current_terminal_layout == 8:
        Terminal().terminal_8()
    elif config.current_terminal_layout == 9:
        Terminal().terminal_9()

    console.print(terminal.get_prompt())


# clear console
def clear(*args):
    os.system("cls" if os.name == "nt" else "clear")


def main():
    console.clear()
    ascii_banner = pyfiglet.figlet_format("PyShell")
    print(ascii_banner)

    # Objects
    cmds = Commands()
    task = Task()
    weather = Weather()
    stock = Stock()
    terminl = Terminal()
    git = Git()
    eq = Equations()
    stats = StatisticsCalculator()
    graph = GraphPlotter()

    commands = {
        "rename": cmds.rename_item,
        "move": cmds.move_file,
        "copy": cmds.copy_file,
        "processes": list_processes,
        "kill": kill_process,
        "network": cmds.network_info,
        "copytext": clipboard_copy,
        "paste": clipboard_paste,
        "password": generate_password,
        "calc": cmds.calculator,
        "stats": lambda args: stats.calculate_statistics(),
        "equation": eq.solve_equation,
        "differential": lambda args: eq.solve_differential(args),
        "math-help": cmds.math_help,
        "weather": weather.get_weather,
        "stock": stock.get_stock_info,
        "stocks": stock.get_multiple_stocks,
        "schedule": task.schedule_task,
        "tasks": task.list_scheduled_tasks,
        "unschedule": task.remove_scheduled_task,
        "stop": task.stop_running_tasks,
        "cls": clear,
        "terminal": terminl.change_terminal,
        "game": lambda args: Game.play_game(" ".join(args)),
        "plot": lambda args: graph.run(),
        "exit": lambda _: exit(),
        "bulk-rename": lambda args: BulkRenamer.bulk_rename(
            path=Prompt.ask("Path of folder"),
            prefix=Prompt.ask("Prefix", default=""),
            suffix=Prompt.ask("Suffix", default=""),
            replace_from=Prompt.ask("replace_from", default=""),
            replace_to=Prompt.ask("replace_to", default=""),
            number=Prompt.ask("Want numbered files?", choices=["y","n"], default="n") == "y",
            new_extension=Prompt.ask("New extension (for eg .txt , .docx)", default="")
        ),
        "ping": lambda args: ping(args[0]),
        "prompt": lambda args: prompt.run(),
        
        # Git Commands (Using Git Class)
        "git-status": git.git_status,
        "git-branches": git.git_branches,
        "git-create": git.git_create_branch,
        "git-switch": git.git_switch_branch,
        "git-push": git.git_push,
        "git-pull": git.git_pull,
        "git-merge": git.git_merge,
        "git-delete": git.git_delete_branch,
        "git-clone": git.git_clone,
        "git-add": git.git_add,
        "git-commit": git.git_commit,
        # Unique Git Features
        "play": lambda args: Song.play_song(" ".join(args)),
        "git-smart": git.git_smart_commit,
        "git-help": git.git_help,
        "git-history": git.git_history,
        "git-undo": git.git_undo,
        "git-stash": git.git_stash,
        "git-recover": git.git_recover,
        "git-dashboard": git.git_dashboard,
        "git-auto_merge": git.git_auto_merge,
        "git-voice": git.git_voice_command,
        "git-reminder": git.git_reminder,
        "git-offline_sync": git.git_offline_sync,
        "search": lambda args: FileSearcher().search(args),
    }

    scheduler_thread = threading.Thread(target=Task().run_scheduler, daemon=True)
    scheduler_thread.start()

    while True:
        display_prompt()
        command = input().strip().lower().split()

        if not command:
            continue

        cmd, *args = command

        start_time = time.time()

        if not command:
            continue

        cmd, *args = command
        start_time = time.time()

        if cmd in commands:
            commands[cmd](args)
        else:
            if cmd == "ls":
                cmds.list_files()
            elif cmd == "touch" and args:
                cmds.create_file(args[0])
            elif cmd == "rm" and args:
                cmds.delete_file(args[0])
            elif cmd == "mkdir" and args:
                cmds.create_folder(args[0])
            elif cmd == "rmdir" and args:
                cmds.delete_folder(args[0])
            elif cmd == "cd" and args:
                cmds.change_directory(args[0])
            elif cmd == "edit" and args:
                cmds.text_editor(args[0])
            elif cmd == "sysinfo":
                cmds.system_info()
            elif cmd == "exit":
                console.print("Exiting PyShell...", style="bold red")
                break
            else:
                console.print("Invalid command!", style="bold red")

        exec_time = time.time() - start_time
        console.print(f"Execution time: {exec_time:.4f} seconds", style="bold yellow")
        time.sleep(1)


if __name__ == "__main__":
    main()
