from datetime import datetime
from rich.live import Live
from rich.panel import Panel
from rich.console import Console
from rich import print


import os
import sys
sys.path.append(os.path.abspath('.'))

from src.config import get_config
config=get_config()

from src.utils import make_dir_not_exist

class logs:
    def __init__(self) -> None:
        self.log_file = config['log_path']

    def log_error(self, s):
        '''
        Logs error messages in the format [datetime] [ERROR] [message] to the console and app.log file
        '''
        message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] {s}"
        print(message)
        make_dir_not_exist(self.log_file)
        with open(self.log_file, "a") as f:
            f.write(message + "\n")

    def log_info(self, s, border_style=None, title = None,subtitle = None):
        '''
        Logs info messages in the format [datetime] [message] to the console and app.log file
        '''
        message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {s}"
        if border_style is None:
            print(message)
        else:
            print(Panel(
                    message, 
                    title=title, 
                    subtitle=subtitle,
                    border_style=border_style,  # Changes the border color and style
                    padding=(1, 2),             # Adds padding inside the box (top-bottom, left-right)
                ))
        make_dir_not_exist(self.log_file)
        with open(self.log_file, "a") as f:
            f.write(message + "\n")