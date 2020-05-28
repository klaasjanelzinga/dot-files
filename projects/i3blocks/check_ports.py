#!/usr/bin/python3
import asyncio
import enum
import json
import logging
import os
import selectors
import socket
import sys
from contextlib import closing
from dataclasses import dataclass, field
from fcntl import fcntl, F_GETFL, F_SETFL
from typing import List, Dict, Tuple

from i3blocks import MouseClick, start_event_loop

logging.basicConfig(filename="/home/klaasjan/projects/i3blocks/time-debug.log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class OutputText(enum.Enum):
    FAILED = "🔻"  # Contains unicode.
    OK = "👍"


@dataclass
class Check:
    type: str
    port: int
    description: str
    host: str
    group_name: str


@dataclass
class Group:
    name: str
    checks: List[Check] = field(default_factory=list)


@dataclass
class Config:
    check_version: str
    groups: List[Group] = field(default_factory=list)


class Settings:

    def __init__(self):
        with open('check_ports_config.json', 'r') as file:
            settings = json.load(file)
            self.config = Config(check_version=settings['check_version'])
            for group in settings['groups']:
                config_group = Group(name=group['name'])
                self.config.groups.append(config_group)
                for check in group['checks']:
                    config_check = Check(type=check['type'],
                                         port=check['port'],
                                         description=check['description'],
                                         host=check['host'],
                                         group_name=config_group.name)
                    config_group.checks.append(config_check)


class RawResult(enum.Enum):
    FAILED = 1
    TIMED_OUT = 2
    SUCCESS = 3


@dataclass
class CheckResult:
    check: Check
    result: RawResult

    def is_ok(self):
        return self.result == RawResult.SUCCESS

    def has_failed(self):
        return not self.is_ok()

    @staticmethod
    def ok(check: Check):
        return CheckResult(check=check, result=RawResult.SUCCESS)

    @staticmethod
    def failed(check: Check):
        return CheckResult(check=check, result=RawResult.FAILED)


@dataclass
class TcpChecker:
    check: Check

    def do_check(self) -> CheckResult:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(15)
            if sock.connect_ex((self.check.host, self.check.port)) == 0:
                return CheckResult.ok(check=self.check)
        return CheckResult.failed(check=self.check)


class Mode(enum.Enum):
    SHORT = 1
    LONG = 2


@dataclass
class CheckPortsTextualResult:
    short: str
    long: str


def check_ports(settings: Settings) -> CheckPortsTextualResult:
    failed_checks: List[Check] = []
    group_status: Dict[str, str] = {}
    for group in settings.config.groups:
        tcp_checkers = [TcpChecker(check=check) for check in group.checks if check.type == 'tcp']
        tcp_check_results = [tcp_check.do_check() for tcp_check in tcp_checkers]
        tcp_check_success = [tcp_check_result for tcp_check_result in tcp_check_results if tcp_check_result.is_ok()]
        tcp_check_fails = [tcp_check_result for tcp_check_result in tcp_check_results if tcp_check_result.has_failed()]
        failed_checks.extend(
            [tcp_check_result.check for tcp_check_result in tcp_check_results if tcp_check_result.has_failed()]
        )
        group_status[group.name] = OutputText.OK.value if len(tcp_check_fails) == 0 else OutputText.FAILED.value

    failed = (", ".join([f"{failed_check.description}[{failed_check.group_name}]"
                         for failed_check in failed_checks])
              if len(failed_checks) > 0
              else "All is well"
              )
    return CheckPortsTextualResult(short=" ".join({k[1] for k in group_status.items()}), long=failed)


def main():
    settings = Settings()
    current_mode = Mode.SHORT

    def callback(mouseclick: MouseClick):
        nonlocal current_mode
        current_mode = Mode.SHORT

    while True:
        short_message, long_message = check_ports(settings)
        if current_mode == Mode.SHORT:
            print(short_message)
        elif current_mode == Mode.LONG:
            print(short_message)

        start_event_loop(timeout=1, callback=callback)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.error("Halting program", ex)
