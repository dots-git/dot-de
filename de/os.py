import pickle
from de.file_utils import working_dir, files_root
from de.utils import print_dict

class os:
    configs: 'dict[dict | ConfValue]' = {}
    files_to_run = []
    def load_configs():
        os.configs = pickle.load(open(working_dir() + '/config/config', 'rb'))
    
    def save_config():
        pickle.dump(os.configs, open(working_dir() + '/config/config', 'wb'))

    def run_script(path, x = 0, y = 0, w = 0, h = 0):
        os.files_to_run.append((files_root() + path, x, y, w, h))

    def print_full_configs():
        print_dict(os.configs)


class ConfValue:
    def __init__(self, value, properties: dict = {}):
        self.value = value
        self.properties = properties
    
    def get(self):
        return self.value
    
    def set(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)