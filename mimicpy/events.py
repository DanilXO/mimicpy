from abc import ABC, abstractmethod
import time
from typing import Union

from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController

class Event(ABC):
    def __init__(self) -> None:
        self.time = time.monotonic()

    @abstractmethod
    def play(self, controller: Union[MouseController, KeyboardController]):
        raise NotImplementedError("Event have to implement play method.")

    @abstractmethod
    def to_dict():
        raise NotImplementedError("Event have to implement to_dict method.")

    def __repr__(self) -> str:
        return f"Event({self.time})"  
    

class MouseMove(Event):
    def __init__(self, x: Union[int, float], y: Union[int, float],
                 position: tuple[Union[int, float]]) -> None:
        super().__init__()
        self._x = x
        self._y = y
        self._position = position
    
    def play(self, controller: MouseController) -> None:
        controller.position = self._position
        controller.move(self._x, self._y)

    def to_dict(self):
        return {
            "name": self.__class__.__name__,
            "x": self._x,
            "y": self._y,
            "position": self._position,
        }
    
    def __repr__(self) -> str:
        return f"MouseMove({self._x},{self._y})"

class MouseClick(Event):
    def __init__(self, x: Union[int, float], y: Union[int, float], 
                 button: Union[Button, int], pressed: bool, 
                 position: tuple[Union[int, float]]) -> None:
        super().__init__()
        self._x = x
        self._y = y
        self._button = button
        self._pressed = pressed
        self._position = position

    def to_dict(self):
        return {
            "name": self.__class__.__name__,
            "x": self._x,
            "y": self._y,
            "pressed": self._pressed,
            "button": str(self._button),
            "position": self._position,
        }
        
    def play(self, controller: MouseController) -> None:
        controller.position = self._position
        controller.click(self._button, 1)

    def __repr__(self) -> str:
        return f"MouseClick({self._x},{self._y},{self._button},{self._pressed})"

class MouseScroll(Event):
    def __init__(self, x: Union[int, float], y: Union[int, float], 
                 dx: Union[int, float], dy: Union[int, float],
                 position: tuple[Union[int, float]]) -> None:
        super().__init__()
        self._x = x
        self._y = y
        self._dx = dx
        self._dy = dy
        self._position = position

    def play(self, controller: MouseController) -> None:
        controller.position = self._position
        controller.scroll(self._dx, self._dy)

    def to_dict(self):
        return {
            "name": self.__class__.__name__,
            "x": self._x,
            "y": self._y,
            "dx": self._dx,
            "dy": self._dy,
            "position": self._position,
        }

    def __repr__(self) -> str:
        return f"MouseScroll({self._x},{self._y},{self._dx},{self._dy})"

class KeyboardPress(Event):
    def __init__(self, key: Union[str, Key]) -> None:
        super().__init__()
        self._key = key
    
    def play(self, controller: KeyboardController) -> None:
        controller.press(self._key)

    def to_dict(self):
        return {
            "name": self.__class__.__name__,
            "key": str(self._key),
        }

    def __repr__(self) -> str:
        return f"KeyboardPress({self._key})"

class KeyboardRelease(Event):
    def __init__(self, key: Union[str, Key]) -> None:
        super().__init__()
        self._key = key
    
    def play(self, controller: KeyboardController) -> None:
        controller.release(self._key)

    def to_dict(self):
        return {
            "name": self.__class__.__name__,
            "key": str(self._key),
        }
    def __repr__(self) -> str:
        return f"KeyboardRelease({self._key})"

