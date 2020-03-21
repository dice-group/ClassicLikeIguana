import subprocess
import time
from datetime import datetime
from subprocess import Popen
from typing import List

from classiclikeiguana.QueryStatistics import QueryStatistics
from classiclikeiguana.read_stdout_until import read_stdout_until, ExecutionMetrics

seconds = float
milliseconds = float


def execute(cli_config: dict) -> object:
    command = cli_config["command"]
    initFinished = cli_config["initFinished"]
    queryFinished = cli_config["queryFinished"]
    queryError: List[str] = cli_config["queryError"]
    queryFile = cli_config["queryFile"]
    timeout: seconds = milliseconds(cli_config["timeout"]) / 1000.0
    timeout_duration: seconds = milliseconds(cli_config["timelimit"]) / 1000.0

    with open(queryFile, 'r') as fp:
        queries: List[str] = fp.readlines()
    queries = [query.strip() for query in queries]
    queries = [query for query in queries if not query == ""]

    def startup_triplestore() -> Popen:
        process: Popen = Popen([command],
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               shell=True,
                               universal_newlines=True)
        startup: ExecutionMetrics = read_stdout_until(process, initFinished, ["none"], 0)
        assert startup.succeeded
        return process

    execution_results: List[QueryStatistics] = [QueryStatistics(queryID, timeout) for queryID in range(len(queries))]
    process: Popen = startup_triplestore()
    query_iter = zip(execution_results, queries)
    start_datetime: datetime = datetime.now()
    start_time = time.time()
    while time.time() < start_time + timeout_duration:
        try:
            query_statistics, query = next(query_iter)
        except StopIteration:
            query_iter = zip(execution_results, queries)
            query_statistics, query = next(query_iter)
        process.stdin.write(query + "\n")
        process.stdin.flush()
        query_execution: ExecutionMetrics = read_stdout_until(process, queryFinished, queryError, timeout)

        query_statistics.add_execution(query_execution)

        if not query_execution.succeeded:
            print("{} || {}".format(query_statistics.queryID, query_execution))
        if not query_execution.succeeded and query_execution.duration == timeout:
            restart_begin = time.time()
            process.kill()
            process.communicate()
            process = startup_triplestore()
            restart_end = time.time()
            timeout_duration += (restart_end - restart_begin)
    process.kill()
    process.communicate()  # EOF
    return start_datetime, execution_results
