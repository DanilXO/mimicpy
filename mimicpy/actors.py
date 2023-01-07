import json
import os
from threading import Lock
from time import sleep
import time
from typing import Optional

from pynput.mouse import Listener as MouseListener, Controller as MouseController
from pynput.keyboard import Listener as KeyboardListener, Key, Controller as KeyboardController

from mimicpy.events import (Event, KeyboardPress, KeyboardRelease, MouseClick, 
                            MouseMove, MouseScroll)
from mimicpy.constants import BUTTON_MAP, KEY_MAP, SCENARIOS_PATH

class Trainer:
    def __init__(self, scenarios_path: str = SCENARIOS_PATH) -> None:
        self._events = []
        self._lock = Lock()
        self.__schould_stop: bool = False
        self._scenarios_path = scenarios_path
    
    @property
    def _schould_stop(self):
        with self._lock:
            return self.__schould_stop

    @_schould_stop.setter
    def _schould_stop(self, value: bool):
        with self._lock:
            self.__schould_stop = value
    
    def learn(self) -> list[Event]:
        mouse_listener = MouseListener(
            on_move=self._mouse_on_move,
            on_click=self._mouse_on_click,
            on_scroll=self._mouse_on_scroll)
        keyboard_listener = KeyboardListener(
            on_press=self._keyboard_on_press,
            on_release=self._keyboard_on_release)
        mouse_listener.start()
        keyboard_listener.start()
        while not self._schould_stop:
            sleep(1)
        mouse_listener.stop()
        keyboard_listener.stop()
        return self._events
    
    def save_scenario(self, path: Optional[str] = None) -> str:
        if path is None:
            file_name = f"scenario_{time.time()}.json"
            path = os.path.join(self._scenarios_path, file_name)

        data = [event.to_dict() for event in self._events]
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path
            
    def _add_event(self, event: Event) -> None:
        with self._lock:
            self._events.append(event)

    def _mouse_on_move(self, x, y) -> Optional[bool]:
        controller = MouseController()
        event = MouseMove(x, y, position=controller.position)
        self._add_event(event)

    def _mouse_on_click(self, x, y, button, pressed) -> Optional[bool]:
        controller = MouseController()
        event = MouseClick(x, y, button, pressed, position=controller.position)
        self._add_event(event)
    
    def _mouse_on_scroll(self, x, y, dx, dy) -> Optional[bool]:
        controller = MouseController()
        event = MouseScroll(x, y, dx, dy, position=controller.position)
        self._add_event(event)

    def _keyboard_on_press(self, key) -> Optional[bool]:
        if key == Key.esc:
            self._schould_stop = True
            return False
        event = KeyboardPress(key)
        self._add_event(event)
    
    def _keyboard_on_release(self, key) -> Optional[bool]:
        event = KeyboardRelease(key)
        self._add_event(event)


class Actor:
    mouse_events = (MouseClick, MouseMove, MouseScroll)
    keyboard_events = (KeyboardPress, KeyboardRelease)
    event_map = {
        MouseMove.__name__: MouseMove,
        MouseScroll.__name__: MouseScroll,
        MouseClick.__name__: MouseClick,
        KeyboardPress.__name__: KeyboardPress,
        KeyboardRelease.__name__: KeyboardRelease
    }

    def __init__(self) -> None:
        self._keyboard = KeyboardController()
        self._mouse = MouseController()

    def play_scenario(self, scenario_path: str) -> None:
        events = self._load_scenario(scenario_path)
        self.play_events(events)

    def _load_scenario(self, scenario_path: str) -> list[Event]:
        with open(scenario_path) as fp:
            data = json.load(fp)
        events = []
        for raw_event in data:
            cls_name = raw_event.pop("name", None)
            if cls_name:
                pop_button = raw_event.pop("button", None)
                if pop_button:
                    button_enum = BUTTON_MAP.get(pop_button, None)
                    if button_enum:
                        raw_event["button"] = button_enum
                    else:
                        raw_event["button"] = pop_button

                pop_key = raw_event.pop("key", None)
                if pop_key:
                    key_enum = KEY_MAP.get(pop_key, None)
                    if key_enum:
                        raw_event["key"] = key_enum
                    else:
                        raw_event["key"] = pop_key

                event_cls = self.event_map.get(cls_name)
                events.append(event_cls(**raw_event))
        return events

        
    def play_events(self, events: list[Event]):
        for idx, event in enumerate(events):
            if isinstance(event, self.mouse_events):
                event.play(controller=self._mouse)
            elif isinstance(event, self.keyboard_events):
                event.play(controller=self._keyboard)
            else:
                continue

            try:
                next_event = events[idx + 1]
                timout_seconds = next_event.time - event.time
            except IndexError:
                timout_seconds = 0.1
            time.sleep(timout_seconds)
