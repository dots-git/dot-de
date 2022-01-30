import pickle
from de.scripts.file_utils import script_root, files_root
import sys

class config:
    configs = {}
    all_windows = []
    files_to_run = []
    def load():
        config.configs = pickle.load(open(script_root() + '/config/config', 'rb'))
    
    def save():
        pickle.dump(config.configs, open(script_root() + '/config/config', 'wb'))

    def run_script(path):
        config.files_to_run.append(files_root() + path)
        print(files_root() + path)