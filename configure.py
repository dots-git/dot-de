import pygame
from de.os import *

os.load_configs()

os.configs['Window']['Header']['Color'] = ConfValue(pygame.Color(10, 20, 50), {'input_type': 'color_selector', 'value_type': pygame.Color})

os.print_full_configs()
os.save_config()

# Colors:
# os.configs['...'] = ConfValue(pygame.Color(0, 0, 0), {'input_type': 'color_selector', 'value_type': pygame.Color})
#
# Integers:
# os.configs['...'] = ConfValue(0, {'min': 0, 'max': 0, 'input_type': 'slider', 'value_type': int})
#
# Remove Key:
# os.configs['...'].pop('Key')