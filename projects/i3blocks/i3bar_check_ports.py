#!/usr/bin/python3
import enum
import json
import logging
import socket
import subprocess
import sys
import urllib.request
from contextlib import closing
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from i3blocks import MouseClick, start_event_loop, Spinner, LongTextDisplayer

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
    port: Optional[int]
    description: str
    host: Optional[str]
    path: Optional[str]
    method: Optional[str]
    scheme: Optional[str]
    command: Optional[str]
    group_name: str


@dataclass
class Group:
    name: str
    checks: List[Check] = field(default_factory=list)


@dataclass
class Config:
    check_version: str
    default_timeout: float
    groups: List[Group] = field(default_factory=list)


class Settings:

    def __init__(self):
        with open('i3bar_check_ports.json', 'r') as file:
            settings = json.load(file)
            self.config = Config(check_version=settings['check_version'], default_timeout=settings['default_timeout'])
            for group in settings['groups']:
                config_group = Group(name=group['name'])
                self.config.groups.append(config_group)
                for check in group['checks']:
                    config_check = Check(type=check['type'],
                                         port=check.get('port'),
                                         description=check['description'],
                                         host=check.get('host'),
                                         path=check.get('path'),
                                         method=check.get("method"),
                                         command=check.get("command"),
                                         scheme=check.get("scheme"),
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


@dataclass
class HttpChecker:
    check: Check

    def do_check(self) -> CheckResult:
        url = f"{self.check.scheme}://{self.check.host}:{self.check.port}{self.check.path}"
        req = urllib.request.Request(url, method=self.check.method)
        try:
            code = urllib.request.urlopen(req, timeout=.1).getcode()
            if code < 300:
                return CheckResult.ok(self.check)
        except Exception:
            pass
        return CheckResult.failed(self.check)


@dataclass
class BashChecker:
    check: Check

    def do_check(self) -> CheckResult:
        command = self.check.command
        try:
            completed_process = subprocess.run(['bash', "-c", command], capture_output=True)
            if completed_process.returncode == 0:
                return CheckResult.ok(self.check)
        except Exception:
            pass
        return CheckResult.failed(self.check)


class Mode(enum.Enum):
    SHORT = 1
    LONG = 2


@dataclass
class CheckResultPerGroup:
    any_group_in_flux: bool
    groups: List[str]
    failed_checks_per_group: Dict[str, List[CheckResult]]
    success_checks_per_group: Dict[str, List[CheckResult]]

    def succes_count_for_group(self, group: str) -> int:
        return len(self.success_checks_per_group[group])

    def failure_count_for_group(self, group: str) -> int:
        return len(self.failed_checks_per_group[group])


def check_ports(settings: Settings) -> CheckResultPerGroup:
    failed_checks: Dict[str, List[CheckResult]] = {}
    succeeded_checks: Dict[str, List[CheckResult]] = {}
    any_group_in_flux = False
    for group in settings.config.groups:
        tcp_checkers = [TcpChecker(check=check) for check in group.checks if check.type == 'tcp']
        http_checkers = [HttpChecker(check=check) for check in group.checks if check.type == 'http']
        bash_checkers = [BashChecker(check=check) for check in group.checks if check.type == 'bash']

        check_results = [tcp_check.do_check() for tcp_check in tcp_checkers]
        check_results.extend([http_check.do_check() for http_check in http_checkers])
        check_results.extend([bash_check.do_check() for bash_check in bash_checkers])

        failed = [tcp_check_result for tcp_check_result in check_results if tcp_check_result.has_failed()]
        ok = [tcp_check_result for tcp_check_result in check_results if tcp_check_result.is_ok()]
        failed_checks[group.name] = failed
        succeeded_checks[group.name] = ok
        if len(ok) > 0 and len(failed) > 0:
            any_group_in_flux = True

    return CheckResultPerGroup(any_group_in_flux=any_group_in_flux,
                               groups=[group.name for group in settings.config.groups],
                               failed_checks_per_group=failed_checks,
                               success_checks_per_group=succeeded_checks)


def create_short_message(result: CheckResultPerGroup, spinners: Dict[str, Spinner]) -> str:
    def group_to_short_text(group: str) -> str:
        successes = result.succes_count_for_group(group)
        fails = result.failure_count_for_group(group)
        if fails > 0 and successes > 0:
            if group not in spinners:
                spinners[group] = Spinner()
            spinner = spinners[group]
            return spinner.next_value()
        elif successes == 0:
            return OutputText.FAILED.value
        elif fails == 0:
            return OutputText.OK.value

    return " ".join([group_to_short_text(group) for group in result.groups])


def create_long_message(result: CheckResultPerGroup) -> str:
    all_failures = [item for sublist in result.failed_checks_per_group.values() for item in sublist]
    if len(all_failures) == 0:
        return "All is well, no failures"
    return ", ".join(
        [f"{failed_check.check.host}:{failed_check.check.port} - {failed_check.check.description} ({failed_check.check.group_name})"
         for failed_check in all_failures])


def main():
    settings = Settings()
    spinners: Dict[str, Spinner] = {}
    current_mode = Mode.SHORT
    default_timeout = settings.config.default_timeout
    timeout = default_timeout
    long_text_displayer = LongTextDisplayer(max_chars=50)

    def callback(mouseclick: MouseClick):
        nonlocal current_mode
        if current_mode == Mode.SHORT:
            current_mode = Mode.LONG
        else:
            current_mode = Mode.SHORT

    while True:
        result = check_ports(settings)
        if current_mode == Mode.SHORT:
            print(create_short_message(result, spinners))
        elif current_mode == Mode.LONG:
            long_text = create_long_message(result)
            long_text_displayer.set_text(long_text)
            print(long_text_displayer.windowed_text())
        sys.stdout.flush()

        # Set timeout to fast if any group is in flux.
        if result.any_group_in_flux:
            timeout = .1
        elif current_mode == Mode.LONG:
            timeout = .5
        else:
            timeout = default_timeout
        start_event_loop(timeout=timeout, callback=callback)


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.error("Halting program", ex)
