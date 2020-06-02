import enum
import os
import selectors
import sys
from fcntl import fcntl, F_GETFL, F_SETFL
from typing import Optional


class MouseClick(enum.Enum):
    LEFT = 1
    MID = 2
    RIGHT = 3
    UP = 4
    DOWN = 5


def got_keyboard_data(file) -> Optional[MouseClick]:
    try:
        read = file.read()
        if read:
            click = int(read.strip())
            return MouseClick(click)
        return None
    except:
        return None


def start_event_loop(timeout: float, callback):
    orig_fl = fcntl(sys.stdin, F_GETFL)
    fcntl(sys.stdin, F_SETFL, orig_fl | os.O_NONBLOCK)
    stdin_selector = selectors.DefaultSelector()
    stdin_selector.register(sys.stdin, selectors.EVENT_READ, None)

    for k, event in stdin_selector.select(timeout=timeout):
        mouse_click = got_keyboard_data(k.fileobj)
        callback(mouse_click)


class Spinner:

    def __init__(self):
        self.spinner = "⠁⠂⠄⡀⢀⠠⠐⠈"
        self.spinner_index = 0
        self.hold_offset = 1

    def next_value(self) -> str:
        self.spinner_index = self.spinner_index + 1 if self.spinner_index + 1 < len(self.spinner) else 0
        return self.spinner[self.spinner_index]

    def hold_value(self) -> str:
        self.spinner_index = self.spinner_index + self.hold_offset if self.spinner_index + 1 < len(self.spinner) else 0
        self.hold_offset *= -1
        return self.spinner[self.spinner_index]


class LongTextDisplayer:

    def __init__(self, max_chars: int):
        self.max_chars = max_chars
        self.text = ""
        self.window_start = 0
        self.window_hold_counter = 0

    def set_text(self, text):
        if self.text != text:
            self.window_start = 0
            self.text = text

    def windowed_text(self):
        if len(self.text) > self.max_chars:
            result = self.text[self.window_start:self.max_chars + self.window_start]
            if self.window_start == 0:
                self.window_hold_counter += 1
                if self.window_hold_counter > 10:
                    self.window_hold_counter = 0
                    self.window_start = 1
            elif self.window_start + self.max_chars - 5 > len(self.text):
                self.window_hold_counter += 1
                if self.window_hold_counter > 10:
                    self.window_hold_counter = 0
                    self.window_start = 0
            else:
                self.window_start += 1
            return result
        return self.text
