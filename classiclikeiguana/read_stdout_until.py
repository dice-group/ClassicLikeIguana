import time
from typing import List

from classiclikeiguana.timeout import timeout


class ExecutionMetrics:
    def __init__(self, duration, succeeded: bool, lines: int, error: str = str()):
        self.duration = duration
        self.succeeded: bool = succeeded
        self.lines: int = lines
        self.error: str = error

    def __str__(self):
        return "succeeded: {succeeded} ; lines: {lines} ; duration: {duration} s ; error: {error}" \
            .format(succeeded=self.succeeded, lines=self.lines, duration=self.duration, error=self.error)


def read_stdout_until(process, success_startswith: str, failure_startswith: List[str], timeout_time: float):
    start = time.time()
    line: str = ""
    lines: int = 0
    duration = None
    succeeded: bool = False
    error: str = ""
    with timeout(timeout_time):
        while True:
            line = process.stdout.readline()
            # print(line, end="")
            if line.startswith(success_startswith):
                duration = time.time() - start
                succeeded = True
                break
            elif any(line.startswith(start_str) for start_str in failure_startswith):
                duration = time.time() - start
                error = line
                succeeded = False
                break
            else:
                lines += 1
    if duration is None:
        duration = timeout_time
    return ExecutionMetrics(duration, succeeded, lines, error)
