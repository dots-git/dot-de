import pickle
from de.file_utils import working_dir, files_root
import sys

class config:
    configs = {}
    files_to_run = []
    def load():
        config.configs = pickle.load(open(working_dir() + '/config/config', 'rb'))
    
    def save():
        pickle.dump(config.configs, open(working_dir() + '/config/config', 'wb'))

    def run_script(path):
        config.files_to_run.append(files_root() + path)
