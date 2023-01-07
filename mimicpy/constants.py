from pynput.keyboard import Key
from pynput.mouse import Button

SCENARIOS_PATH = "scenarios"

KEY_MAP = {str(enum_val): enum_val for enum_val in Key}
BUTTON_MAP = {str(enum_val): enum_val for enum_val in Button}
