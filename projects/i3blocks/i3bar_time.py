#!/usr/bin/python3
import datetime
import enum
import logging
import os
import selectors
import sys
from datetime import datetime, timedelta
from fcntl import fcntl, F_SETFL, F_GETFL
from typing import Optional

from time import monotonic

logging.basicConfig(filename="/home/klaasjan/projects/i3blocks/time-debug.log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MouseClick(enum.Enum):
    LEFT = 1
    MID = 2
    RIGHT = 3
    UP = 4
    DOWN = 5


class Mode(enum.Enum):
    TIME = "time-mode"
    STOPWATCH_STOPPED = "stopwatch-mode"
    STOPWATCH_RUNNING = "stopwatch-running-mode"
    STOPWATCH_READY = "stopwatch-ready"
    STOPWATCH_LAP = "stopwatch-lap"


def got_keyboard_data(file) -> Optional[MouseClick]:
    try:
        read = file.read()
        if read:
            click = int(read.strip())
            return MouseClick(click)
        return None
    except:
        return None


class Stopwatch:

    def __init__(self):
        self.value = 0.0
        self.started_at = 0
        self.last_lap = 0.0

    def start(self) -> None:
        self.started_at = monotonic()
        self.value = 0

    def stop(self) -> None:
        self.value = monotonic() - self.started_at

    def current_value(self) -> str:
        return str(timedelta(seconds=monotonic() - self.started_at))

    def final_value(self) -> str:
        return str(timedelta(seconds=self.value))

    def lap_value(self) -> str:
        return str(timedelta(seconds=self.last_lap))

    def lap(self):
        self.last_lap = monotonic() - self.started_at

    def reset(self):
        self.value = 0.0
        self.started_at = 0
        self.last_lap = 0.0


class DatetimeFormatPicker:

    @staticmethod
    def print_in_normal_short_format() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M")

    @staticmethod
    def print_in_normal_format() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def print_in_short_format():
        return datetime.now().strftime("%d %B %H:%M")

    @staticmethod
    def print_in_short_short_format():
        return datetime.now().strftime("%d-%m %H:%M")

    @staticmethod
    def print_in_b_format():
        return datetime.now().strftime("%d %B %Y %H:%M:%S")

    @staticmethod
    def print_in_iso_format():
        return datetime.now().isoformat()

    def __init__(self):
        self.format_index = 0
        self.display_functions = [
            DatetimeFormatPicker.print_in_normal_format,
            DatetimeFormatPicker.print_in_normal_short_format,
            DatetimeFormatPicker.print_in_iso_format,
            DatetimeFormatPicker.print_in_b_format,
            DatetimeFormatPicker.print_in_short_format,
            DatetimeFormatPicker.print_in_short_short_format,
        ]

    def next_format(self):
        self.format_index = self.format_index - 1 if self.format_index > 0 else len(self.display_functions) - 1

    def previous_format(self):
        self.format_index = self.format_index + 1 if self.format_index + 1 < len(self.display_functions) else 0

    def format(self) -> str:
        return self.display_functions[self.format_index]()


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


def main():
    orig_fl = fcntl(sys.stdin, F_GETFL)
    fcntl(sys.stdin, F_SETFL, orig_fl | os.O_NONBLOCK)
    stdin_selector = selectors.DefaultSelector();
    stdin_selector.register(sys.stdin, selectors.EVENT_READ, None)

    current_mode = Mode.TIME
    stopwatch = Stopwatch()
    timeout = 1
    lap_counter = 0
    spinner = Spinner()
    display_format = DatetimeFormatPicker()

    while True:
        logger.debug(f"Current mode {current_mode}")
        if current_mode == Mode.TIME:
            print(display_format.format())
            timeout = 1
        elif current_mode == Mode.STOPWATCH_STOPPED:
            print(f"stopped: {stopwatch.final_value()}")
            timeout = 1
        elif current_mode == Mode.STOPWATCH_RUNNING:
            print(f"{spinner.next_value()} {stopwatch.current_value()}")
            timeout = .1
        elif current_mode == Mode.STOPWATCH_READY:
            print(f"stopwatch: {stopwatch.final_value()}")
            timeout = 1
        elif current_mode == Mode.STOPWATCH_LAP:
            print(f"lap: {spinner.hold_value()} {stopwatch.lap_value()}")
            lap_counter += 1
            if lap_counter > 20:
                current_mode = Mode.STOPWATCH_RUNNING
            timeout = .1
        else:
            logger.error("Out of iffs")
        sys.stdout.flush()

        # Select input from stdin. Using timeout to update the state machine.
        for k, event in stdin_selector.select(timeout=timeout):
            requested = got_keyboard_data(k.fileobj)
            logger.debug(f"requested {requested} {current_mode}")
            if requested == MouseClick.DOWN and current_mode == Mode.TIME:
                # Previous format.
                display_format.previous_format()
            elif requested == MouseClick.UP and current_mode == Mode.TIME:
                # Next format.
                display_format.next_format()
            elif requested == MouseClick.LEFT and current_mode == Mode.TIME:
                # Reset stopwatch.
                current_mode = Mode.STOPWATCH_READY
                stopwatch.reset()
            elif requested == MouseClick.LEFT and current_mode == Mode.STOPWATCH_READY:
                current_mode = Mode.STOPWATCH_RUNNING
                stopwatch.start()
            elif requested == MouseClick.LEFT and current_mode == Mode.STOPWATCH_STOPPED:
                # Start stopwatch.
                current_mode = Mode.STOPWATCH_READY
                stopwatch.reset()
            elif requested == MouseClick.LEFT and current_mode == Mode.STOPWATCH_RUNNING:
                # Stop stopwatch.
                current_mode = Mode.STOPWATCH_STOPPED
                stopwatch.stop()
            elif requested == MouseClick.MID:
                # Reset to time.
                current_mode = Mode.TIME
                stopwatch.reset()
            elif requested == MouseClick.RIGHT and current_mode == Mode.STOPWATCH_RUNNING:
                # Register a lap.
                stopwatch.lap()
                current_mode = Mode.STOPWATCH_LAP
                lap_counter = 0
            else:
                logger.info("No events for this click!")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.error("Halting program", ex)
