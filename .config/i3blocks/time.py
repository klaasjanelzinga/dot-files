#!/usr/bin/python3
import os
import selectors
import sys
from datetime import datetime
from fcntl import fcntl, F_SETFL, F_GETFL


def print_in_normal_short_format():
    current_time = datetime.now()
    print(current_time.strftime("%Y-%m-%d %H:%M"))

def print_in_normal_format():
    current_time = datetime.now()
    print(current_time.strftime("%Y-%m-%d %H:%M:%S"))


def print_in_short_format():
    current_time = datetime.now()
    print(current_time.strftime("%d %B %H:%M"))


def print_in_short_short_format():
    current_time = datetime.now()
    print(current_time.strftime("%d-%m %H:%M"))


def print_in_b_format():
    current_time = datetime.now()
    print(current_time.strftime("%d %B %Y %H:%M:%S"))


def print_in_iso_format():
    current_time = datetime.now()
    print(current_time.isoformat())


def got_keyboard_data(stdin):
    data = stdin.read()
    # with open('debug.txt', 'w+') as f:
        # f.write(data)


def main():
    orig_fl = fcntl(sys.stdin, F_GETFL)
    fcntl(sys.stdin, F_SETFL, orig_fl | os.O_NONBLOCK)
    m_selector = selectors.DefaultSelector()
    m_selector.register(sys.stdin, selectors.EVENT_READ, got_keyboard_data)

    display_functions = [
        print_in_normal_format,
        print_in_normal_short_format,
        print_in_iso_format,
        print_in_b_format,
        print_in_short_format,
        print_in_short_short_format,
    ]

    current_format = 0

    while True:
        display_functions[current_format]()
        sys.stdout.flush()
        for k, mask in m_selector.select(timeout=1):
            k.data(k.fileobj)
            current_format = current_format + 1 if current_format + 1 < len(display_functions) else 0


if __name__ == "__main__":
    main()
