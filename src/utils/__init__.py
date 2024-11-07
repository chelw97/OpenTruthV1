import os

def make_dir_not_exist(path:str):
    '''
    get the folder first then create the folder if the folder does not exist
    '''
    if path.endswith("/"):
        folder = path
    else:
        folder = os.path.dirname(path)
    if not os.path.exists(folder) and folder.strip() != "":
        os.makedirs(folder)