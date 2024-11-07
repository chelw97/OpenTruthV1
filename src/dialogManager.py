import datetime
import json
import os
import sys
sys.path.append(os.path.abspath('.'))

from src.config import get_config
config=get_config()

from src.utils import make_dir_not_exist
from interface.dialogManagerInterface import dialogManagerInterface



class dialogManager(dialogManagerInterface):
    def __init__(self):
        pass

    def write_dialog(self, s, path):
        '''
        Writes dialog in JSON format as per OpenAI's style to a specified file path
        Appends the JSON-structured message to the file.
        example:
            {"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "What's the capital of France?"}, {"role": "assistant", "content": "Paris, as if everyone doesn't know that already."}]}
            {"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "Who wrote 'Romeo and Juliet'?"}, {"role": "assistant", "content": "Oh, just some guy named William Shakespeare. Ever heard of him?"}]}
            {"messages": [{"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."}, {"role": "user", "content": "How far is the Moon from Earth?"}, {"role": "assistant", "content": "Around 384,400 kilometers. Give or take a few, like that really matters."}]}
        '''
        # dialog_structure = {
        #     "messages": [
        #         {"role": "system", "content": "Marv is a factual chatbot that is also sarcastic."},
        #         {"role": "user", "content": s['user']},
        #         {"role": "assistant", "content": s['assistant']}
        #     ]
        # }

        # # Append dialog in JSON format to the file
        # make_dir_not_exist(path)
        # with open(path, "a") as f:
        #     f.write(json.dumps(dialog_structure) + "\n")
        pass

    def read_dialog(self, path):
        pass