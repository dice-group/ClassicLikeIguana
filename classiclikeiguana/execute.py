import atexit
import shlex
import subprocess
import time
from csv import DictWriter
from datetime import datetime
from subprocess import Popen
from typing import List

from classiclikeiguana.QueryStatistics import QueryStatistics
from classiclikeiguana.read_stdout_until import read_stdout_until, ExecutionMetrics
from classiclikeiguana.write_result_file import open_errorfile, write_error_line

seconds = float
milliseconds = float

current_process = None


def execute(cli_config: dict, debug: bool = False) -> object:
    command = cli_config["command"]
    command = shlex.split(command)
    initFinished = cli_config["initFinished"]
    queryFinished = cli_config["queryFinished"]
    queryError: List[str] = cli_config["queryError"]
    queryFile = cli_config["queryFile"]
    timeout_duration: seconds = milliseconds(cli_config["timeout"]) / 1000.0
    timelimit: seconds = milliseconds(cli_config["timelimit"]) / 1000.0

    with open(queryFile, 'r') as fp:
        queries: List[str] = fp.readlines()
    queries = [query.strip() for query in queries]
    queries = [query for query in queries if not query == ""]

    def startup_triplestore() -> Popen:
        process: Popen = Popen(command,
                               stdout=subprocess.PIPE,
                               stdin=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               errors='replace',
                               universal_newlines=True)
        startup: ExecutionMetrics = read_stdout_until(process, initFinished, [], 0)
        assert startup.succeeded
        global current_process
        current_process = process
        return process

    def kill_subprocess():
        current_process.kill()

    atexit.register(kill_subprocess)

    execution_results: List[QueryStatistics] = [QueryStatistics(queryID, timeout_duration) for queryID in
                                                range(len(queries))]
    process: Popen = startup_triplestore()
    query_iter = zip(execution_results, queries)
    start_datetime: datetime = datetime.now()
    error_writer: DictWriter = open_errorfile(cli_config, start_datetime)
    start_time = time.time()
    query_mixes = 0
    while time.time() < start_time + timelimit:
        try:
            query_statistics, query = next(query_iter)
        except StopIteration:
            query_iter = zip(execution_results, queries)
            query_statistics, query = next(query_iter)
            query_mixes += 1
            print("## {}s: {} query mix(es) finished".format(time.time() - start_time, query_mixes))
        if debug: print("## {} {}".format(query_statistics.queryID, query))
        process.stdin.write(query + "\n")
        process.stdin.flush()

        query_execution: ExecutionMetrics = read_stdout_until(process, queryFinished, queryError, timeout_duration,
                                                              debug)

        query_statistics.add_execution(query_execution)

        if not query_execution.succeeded:
            errorprocessing_begin = time.time()
            write_error_line(query_statistics.queryID, error_writer, query_execution, time.time() - start_time)
            if query_execution.timed_out or process.poll() is not None:
                print("## {}s fatal error occurred . restarting triple store.".format(time.time() - start_time))
                process.kill()
                process.communicate(timeout=3)
                process = startup_triplestore()
            errorprocessing_end = time.time()
            timelimit += (errorprocessing_end - errorprocessing_begin)

    process.kill()
    process.communicate()  # EOF
    return start_datetime, execution_results
