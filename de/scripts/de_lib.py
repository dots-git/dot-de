import pickle
from de.scripts.file_utils import script_root

class config:
    configs = {}
    all_windows = []

    def load():
        config.configs = pickle.load(open(script_root() + '/config/config', 'rb'))
    
    def save():
        pickle.dump(config.configs, open(script_root() + '/config/config', 'wb'))
