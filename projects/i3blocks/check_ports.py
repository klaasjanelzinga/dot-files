#!/usr/bin/python3
import enum
import json
import logging
import socket
from contextlib import closing
from dataclasses import dataclass, field
from typing import List

logging.basicConfig(filename="/home/klaasjan/projects/i3blocks/time-debug.log",
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class Check:
    type: str
    port: int
    description: str
    host: str


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
                    config_check = Check(type=check['type'], port=check['port'], description=check['description'],
                                         host=check['host'])
                    config_group.checks.append(config_check)


class RawResult(enum.Enum):
    FAILED = 1
    TIMED_OUT = 2
    SUCCESS = 3


@dataclass
class CheckResult:
    group: str
    host: str
    port: str
    result: RawResult

    @staticmethod
    def ok(group, host, port):
        return CheckResult(group=group, host=host, port=port, result=RawResult.SUCCESS)

    @staticmethod
    def failed(group, host, port):
        return CheckResult(group=group, host=host, port=port, result=RawResult.FAILED)


@dataclass
class TcpChecker:
    group: str
    host: str
    port: int
    description: str

    def check(self) -> CheckResult:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            sock.settimeout(15)
            if sock.connect_ex((self.host, self.port)) == 0:
                return CheckResult.ok(group=self.group, host=self.host, port=self.port)
        return CheckResult.failed(group=self.group, host=self.host, port=self.port)


def main():
    settings = Settings()
    tcp_checkers = [TcpChecker(group=gr.name, host=check.host, port=check.port, description=check.description) for gr in
                    settings.config.groups for check in gr.checks if check.type == 'tcp']
    for tcp_check in tcp_checkers:
        check_result = tcp_check.check()
        if check_result.result == RawResult.SUCCESS:
            print(f"{tcp_check.port} = OK")
        else:
            print(f"{tcp_check.port} = OFFLINE")


if __name__ == "__main__":
    try:
        main()
    except Exception as ex:
        logger.error("Halting program", ex)
