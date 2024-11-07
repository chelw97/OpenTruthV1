import os
import sys
sys.path.append(os.path.abspath('.'))

from src.config import get_config
config=get_config()
from interface.memoryInterface import memoryInterface

class memory(memoryInterface):
    def updat_memory(self):
        pass

    def quer_memory(self):
        return ""