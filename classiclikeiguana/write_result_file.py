import atexit
import json
import os
import random
from csv import DictWriter
from datetime import datetime
from typing import List

from classiclikeiguana.QueryStatistics import QueryStatistics
from classiclikeiguana.read_stdout_until import ExecutionMetrics


def generate_benchmarkID() -> str:
    return str(random.randint(0, int(pow(10, 15))))


def open_errorfile(cli_config, start_datetime) -> DictWriter:
    error_file = open(get_output_filename(cli_config, start_datetime) + "_errors.csv", 'w')
    atexit.register(lambda: error_file.close())
    error_writer = DictWriter(error_file, fieldnames=["queryID", "errortime", "errorline"])

    error_writer.writeheader()
    return error_writer


def write_error_line(queryID: int, error_file: DictWriter, execution_metrics: ExecutionMetrics, passed_time: float):
    for errorline in execution_metrics.error:
        error_file.writerow({
            "queryID": queryID,
            "errortime": passed_time,
            "errorline": errorline.rstrip()
        })


def get_output_filename(cli_config, start_datetime):
    outputfile: str = "CLI_{}_{:02d}-clients_{}_{}".format(cli_config["dataset"], 1, cli_config["triplestore"],
                                                           start_datetime.strftime("%Y-%m-%d_%H-%M-%S"))
    return outputfile


def write_result_file(execution_results: List[QueryStatistics], cli_config: dict, start_datetime: datetime):
    outputfile = get_output_filename(cli_config, start_datetime)

    benchmarkID: str = generate_benchmarkID()

    with open(os.path.join(outputfile + ".json"), "w") as jsonfile:
        jsonfile.write(json.dumps({'benchmarkID': benchmarkID,
                                   'starttime': str(start_datetime),
                                   'runtime': cli_config["timelimit"],
                                   'timeout': cli_config["timeout"],
                                   "format": "CLI",
                                   'dataset': cli_config["dataset"],
                                   'noclients': 1,
                                   'triplestore': cli_config["triplestore"]},
                                  sort_keys=True,
                                  indent=4),
                       )
    fieldnames = ["starttime", "benchmarkID", "format", "dataset", "triplestore", "noclients", "queryID", "qps",
                  "succeeded", "failed", "timeouts", "unknownExceptions", "wrongCodes", "totaltime", "resultsize",
                  "penalizedtime"]
    output_csv = outputfile + ".csv"
    with open(output_csv, 'w') as csvfile:
        csvwriter = DictWriter(csvfile,
                               fieldnames=fieldnames)
        csvwriter.writeheader()
        for query_statistics in execution_results:
            csvwriter.writerow({
                "starttime": start_datetime,
                "benchmarkID": benchmarkID,
                "format": "CLI",
                "dataset": cli_config["dataset"],
                "triplestore": cli_config["triplestore"],
                "noclients": 1,
                "queryID": query_statistics.queryID,
                "qps": query_statistics.qps,
                "succeeded": query_statistics.succeeded,
                "failed": query_statistics.failed,
                "wrongCodes": query_statistics.wrongCodes,
                "unknownExceptions": query_statistics.unknownExceptions,
                "timeouts": query_statistics.timeouts,
                "totaltime": query_statistics.totaltime_ms,
                "resultsize": query_statistics.resultsize if query_statistics.resultsize is not None else '',
                "penalizedtime": query_statistics.penalizedtime_ms
            })
