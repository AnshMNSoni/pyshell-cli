import os
import re
import fnmatch
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich.panel import Panel
import pyperclip
import subprocess

console = Console()

class FileSearcher:
    def __init__(self):
        self.search_results = []
    
    def search(self, args):
        if not args:
            self.show_help()
            return
        
        path = "."
        name_pattern = None
        ext_pattern = None
        min_size = None
        max_size = None
        min_mtime = None
        max_mtime = None
        case_sensitive = False
        recursive = True
        
        i = 0
        while i < len(args):
            arg = args[i]
            
            if arg == "--path" and i + 1 < len(args):
                path = args[i + 1]
                i += 2
            elif arg == "--name" and i + 1 < len(args):
                name_pattern = args[i + 1]
                i += 2
            elif arg == "--ext" and i + 1 < len(args):
                ext_pattern = args[i + 1]
                i += 2
            elif arg == "--min-size" and i + 1 < len(args):
                min_size = self.parse_size(args[i + 1])
                i += 2
            elif arg == "--max-size" and i + 1 < len(args):
                max_size = self.parse_size(args[i + 1])
                i += 2
            elif arg == "--min-mtime" and i + 1 < len(args):
                min_mtime = self.parse_time(args[i + 1])
                i += 2
            elif arg == "--max-mtime" and i + 1 < len(args):
                max_mtime = self.parse_time(args[i + 1])
                i += 2
            elif arg == "--case-sensitive":
                case_sensitive = True
                i += 1
            elif arg == "--no-recursive":
                recursive = False
                i += 1
            elif i == 0 and not arg.startswith("--"):
                name_pattern = arg
                i += 1
            else:
                i += 1
        
        if not os.path.exists(path):
            console.print(f"Path not found: {path}", style="bold red")
            return
        
        self.search_results = []
        
        if recursive:
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if self.match_file(file_path, name_pattern, ext_pattern, 
                                      min_size, max_size, min_mtime, max_mtime, 
                                      case_sensitive):
                        self.search_results.append(file_path)
        else:
            for item in os.listdir(path):
                file_path = os.path.join(path, item)
                if os.path.isfile(file_path):
                    if self.match_file(file_path, name_pattern, ext_pattern, 
                                      min_size, max_size, min_mtime, max_mtime, 
                                      case_sensitive):
                        self.search_results.append(file_path)
        
        self.display_results()
        
        if self.search_results:
            self.interactive_menu()
    
    def parse_size(self, size_str):
        size_str = size_str.lower().strip()
        units = {'b': 1, 'kb': 1024, 'mb': 1024**2, 'gb': 1024**3, 'tb': 1024**4}
        
        for unit, multiplier in units.items():
            if size_str.endswith(unit):
                try:
                    return float(size_str[:-len(unit)]) * multiplier
                except ValueError:
                    pass
        
        try:
            return float(size_str)
        except ValueError:
            console.print(f"Invalid size format: {size_str}", style="bold yellow")
            return None
    
    def parse_time(self, time_str):
        time_str = time_str.strip()
        
        if time_str.endswith('d'):
            try:
                days = int(time_str[:-1])
                from datetime import timedelta
                return (datetime.now() - timedelta(days=days)).timestamp()
            except ValueError:
                pass
        
        formats = [
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(time_str, fmt)
                return dt.timestamp()
            except ValueError:
                continue
        
        console.print(f"Invalid time format: {time_str}", style="bold yellow")
        return None
    
    def match_file(self, file_path, name_pattern, ext_pattern, 
                   min_size, max_size, min_mtime, max_mtime, case_sensitive):
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_name)[1].lower()
        
        try:
            stat = os.stat(file_path)
            file_size = stat.st_size
            file_mtime = stat.st_mtime
        except (OSError, PermissionError):
            return False
        
        if name_pattern:
            if case_sensitive:
                if not fnmatch.fnmatch(file_name, name_pattern):
                    return False
            else:
                if not fnmatch.fnmatch(file_name.lower(), name_pattern.lower()):
                    return False
        
        if ext_pattern:
            ext_pattern = ext_pattern.lower()
            if not ext_pattern.startswith('.'):
                ext_pattern = '.' + ext_pattern
            if file_ext != ext_pattern:
                return False
        
        if min_size is not None and file_size < min_size:
            return False
        
        if max_size is not None and file_size > max_size:
            return False
        
        if min_mtime is not None and file_mtime < min_mtime:
            return False
        
        if max_mtime is not None and file_mtime > max_mtime:
            return False
        
        return True
    
    def format_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024**2:
            return f"{size_bytes / 1024:.1f} KB"
        elif size_bytes < 1024**3:
            return f"{size_bytes / 1024**2:.1f} MB"
        elif size_bytes < 1024**4:
            return f"{size_bytes / 1024**3:.1f} GB"
        else:
            return f"{size_bytes / 1024**4:.1f} TB"
    
    def display_results(self):
        if not self.search_results:
            console.print(Panel("No files found matching your search criteria.", 
                              title="Search Results", style="yellow"))
            return
        
        table = Table(title=f"Search Results ({len(self.search_results)} files found)")
        table.add_column("#", style="cyan", width=4)
        table.add_column("File Name", style="green", width=30)
        table.add_column("Size", style="yellow", width=12)
        table.add_column("Modified", style="magenta", width=20)
        table.add_column("Path", style="white", width=40)
        
        for idx, file_path in enumerate(self.search_results[:50], 1):
            try:
                stat = os.stat(file_path)
                file_name = os.path.basename(file_path)
                file_size = self.format_size(stat.st_size)
                mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
                dir_path = os.path.dirname(file_path)
                
                table.add_row(
                    str(idx),
                    file_name,
                    file_size,
                    mod_time,
                    dir_path
                )
            except Exception:
                continue
        
        console.print(table)
        
        if len(self.search_results) > 50:
            console.print(f"... and {len(self.search_results) - 50} more files", style="dim")
    
    def interactive_menu(self):
        while True:
            console.print("\n[bold cyan]Actions:[/bold cyan]")
            console.print("  [1-999] - Open file by number")
            console.print("  [c#] - Copy file path (e.g., c1, c2)")
            console.print("  [o#] - Open containing folder (e.g., o1, o2)")
            console.print("  [d#] - Delete file (e.g., d1, d2)")
            console.print("  [info#] - Show detailed info (e.g., info1)")
            console.print("  [list] - Show all results again")
            console.print("  [help] - Show search help")
            console.print("  [q/quit] - Exit search mode")
            
            choice = Prompt.ask("\nSelect action").strip().lower()
            
            if choice in ['q', 'quit', 'exit']:
                break
            elif choice == 'list':
                self.display_results()
            elif choice == 'help':
                self.show_help()
            elif choice.startswith('c') and choice[1:].isdigit():
                idx = int(choice[1:]) - 1
                if 0 <= idx < len(self.search_results):
                    file_path = self.search_results[idx]
                    pyperclip.copy(file_path)
                    console.print(f"[bold green]Path copied to clipboard:[/bold green] {file_path}")
                else:
                    console.print("Invalid file number", style="bold red")
            elif choice.startswith('o') and choice[1:].isdigit():
                idx = int(choice[1:]) - 1
                if 0 <= idx < len(self.search_results):
                    file_path = self.search_results[idx]
                    folder_path = os.path.dirname(file_path)
                    self.open_folder(folder_path)
                else:
                    console.print("Invalid file number", style="bold red")
            elif choice.startswith('d') and choice[1:].isdigit():
                idx = int(choice[1:]) - 1
                if 0 <= idx < len(self.search_results):
                    file_path = self.search_results[idx]
                    confirm = Prompt.ask(f"Delete file? {file_path}", choices=["y", "n"], default="n")
                    if confirm == 'y':
                        try:
                            os.remove(file_path)
                            console.print(f"[bold green]File deleted:[/bold green] {file_path}")
                            self.search_results.pop(idx)
                        except Exception as e:
                            console.print(f"[bold red]Error deleting file:[/bold red] {e}")
                else:
                    console.print("Invalid file number", style="bold red")
            elif choice.startswith('info') and choice[4:].isdigit():
                idx = int(choice[4:]) - 1
                if 0 <= idx < len(self.search_results):
                    self.show_file_info(self.search_results[idx])
                else:
                    console.print("Invalid file number", style="bold red")
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(self.search_results):
                    self.open_file(self.search_results[idx])
                else:
                    console.print("Invalid file number", style="bold red")
            else:
                console.print("Invalid command", style="bold red")
    
    def open_file(self, file_path):
        try:
            if os.name == 'nt':
                os.startfile(file_path)
            elif os.name == 'posix':
                subprocess.run(['xdg-open', file_path], check=True)
            else:
                subprocess.run(['open', file_path], check=True)
            console.print(f"[bold green]Opened:[/bold green] {file_path}")
        except Exception as e:
            console.print(f"[bold red]Error opening file:[/bold red] {e}")
    
    def open_folder(self, folder_path):
        try:
            if os.name == 'nt':
                os.startfile(folder_path)
            elif os.name == 'posix':
                subprocess.run(['xdg-open', folder_path], check=True)
            else:
                subprocess.run(['open', folder_path], check=True)
            console.print(f"[bold green]Opened folder:[/bold green] {folder_path}")
        except Exception as e:
            console.print(f"[bold red]Error opening folder:[/bold red] {e}")
    
    def show_file_info(self, file_path):
        try:
            stat = os.stat(file_path)
            file_name = os.path.basename(file_path)
            file_ext = os.path.splitext(file_name)[1] or "(no extension)"
            file_size = stat.st_size
            created_time = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
            modified_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            accessed_time = datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S")
            
            info = f"""[bold cyan]File Information[/bold cyan]

  [bold]Name:[/bold]         {file_name}
  [bold]Extension:[/bold]    {file_ext}
  [bold]Full Path:[/bold]    {file_path}
  [bold]Size:[/bold]         {self.format_size(file_size)} ({file_size:,} bytes)
  [bold]Created:[/bold]      {created_time}
  [bold]Modified:[/bold]     {modified_time}
  [bold]Accessed:[/bold]     {accessed_time}
  [bold]Is File:[/bold]      {os.path.isfile(file_path)}
  [bold]Is Directory:[/bold] {os.path.isdir(file_path)}
  [bold]Is Link:[/bold]      {os.path.islink(file_path)}
  [bold]Absolute:[/bold]     {os.path.isabs(file_path)}
"""
            console.print(Panel(info, style="cyan"))
        except Exception as e:
            console.print(f"[bold red]Error getting file info:[/bold red] {e}")
    
    def show_help(self):
        help_text = """
[bold cyan]File Search Command Help[/bold cyan]

[bold]Usage:[/bold]
  search [options] [pattern]

[bold]Options:[/bold]
  [cyan]--path[/cyan] <path>        : Search in specific directory (default: current)
  [cyan]--name[/cyan] <pattern>      : File name pattern (supports wildcards: *, ?)
  [cyan]--ext[/cyan] <extension>     : File extension (e.g., .txt, .py)
  [cyan]--min-size[/cyan] <size>    : Minimum file size (e.g., 1KB, 5MB, 2GB)
  [cyan]--max-size[/cyan] <size>    : Maximum file size
  [cyan]--min-mtime[/cyan] <time>   : Minimum modification time (e.g., 7d, 2024-01-01)
  [cyan]--max-mtime[/cyan] <time>   : Maximum modification time
  [cyan]--case-sensitive[/cyan]      : Case-sensitive name matching
  [cyan]--no-recursive[/cyan]        : Do not search subdirectories

[bold]Examples:[/bold]
  search *.txt                    : Find all .txt files
  search --name "*.py" --path "src" : Find Python files in src directory
  search --ext .pdf --min-size 1MB : Find PDF files larger than 1MB
  search --min-mtime 7d           : Find files modified in last 7 days
  search --max-mtime "2024-01-01" : Find files modified before 2024-01-01
  search test --no-recursive      : Find files with 'test' in name (current dir only)

[bold]Interactive Commands (after search):[/bold]
  [1-999]  : Open file by number
  [c#]     : Copy file path (e.g., c1, c2)
  [o#]     : Open containing folder (e.g., o1, o2)
  [d#]     : Delete file (e.g., d1, d2)
  [info#]  : Show detailed info (e.g., info1)
  [list]   : Show results again
  [help]   : Show this help
  [q/quit] : Exit search mode

[bold]Size Units:[/bold]
  B, KB, MB, GB, TB (case insensitive)

[bold]Time Formats:[/bold]
  Nd           : N days ago (e.g., 7d, 30d)
  YYYY-MM-DD   : Specific date (e.g., 2024-01-15)
  YYYY-MM-DD HH:MM:SS : Specific date and time
"""
        console.print(Panel(help_text, title="Search Command Help", style="cyan"))
