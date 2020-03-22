import time
from typing import List

from classiclikeiguana.timeout import timeout


class ExecutionMetrics:
    def __init__(self, duration, succeeded: bool, timed_out: bool, lines: int, error: List[str] = None):
        if error is None:
            error = list()
        self.duration = duration
        self.succeeded: bool = succeeded
        self.timed_out: bool = timed_out
        self.lines: int = lines
        self.error: List[str] = error

    def __str__(self):
        return "succeeded: {succeeded} ; lines: {lines} ; duration: {duration} s ; error: {error}" \
            .format(succeeded=self.succeeded, lines=self.lines, duration=self.duration, error=self.error)


def read_stdout_until(process, terminal_startswith: str, failure_startswith: List[str], timeout_time: float,
                      debug: bool = False):
    start = time.time()
    line: str = ""
    lines: int = 0
    duration = None
    succeeded = True
    timed_out = False
    errors: List[str] = list()
    with timeout(timeout_time):
        while True:
            line = process.stdout.readline()
            if debug: print(line, end="")
            for start_str in failure_startswith:
                if line.startswith(start_str):
                    errors.append(line)
                    succeeded = False
            if any(line.startswith(start_str) for start_str in terminal_startswith):
                duration = time.time() - start
                break
            else:
                lines += 1

    if duration is None:
        succeeded = False
        timed_out = True
        duration = timeout_time
    return ExecutionMetrics(duration, succeeded, timed_out, lines, errors)
