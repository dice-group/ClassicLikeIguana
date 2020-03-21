import csv
import json
import os
from datetime import datetime
from random import random
from typing import List

from classiclikeiguana.QueryStatistics import QueryStatistics


def write_result_file(execution_results: List[QueryStatistics], cli_config: dict, start_datetime: datetime):
    outputfile: str = "CLI_{}_{:02d}-clients_{}_{}".format(cli_config["dataset"], 1, cli_config["triplestore"],
                                                           start_datetime.strftime("%Y-%m-%d_%H-%M-%S"))
    benchmarkID = str(random.randint(0, int(pow(10, 15))))
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
        csvwriter = csv.DictWriter(csvfile,
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
