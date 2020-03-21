from classiclikeiguana.read_stdout_until import ExecutionMetrics


class QueryStatistics:

    def __init__(self, queryID, timeout_duration):
        self._penalizedtime = 0
        self._totaltime = 0
        self._resultsize = None
        self._queryID = queryID
        self._timeout_duration = timeout_duration
        self._timeouts = 0
        self._unknownExceptions = 0
        self._wrongCodes = 0
        self._succeeded = 0

    def add_execution(self, execution_metrics: ExecutionMetrics):
        self._totaltime += execution_metrics.duration
        if execution_metrics.succeeded:
            self._penalizedtime += execution_metrics.duration
            self._succeeded += 1
            if self._resultsize is None:
                self._resultsize = execution_metrics.lines
            # todo: what if the triple store doesn't answer deterministically?
        else:
            self._penalizedtime += self.timeout_duration
            if execution_metrics.duration == self.timeout_duration:
                self._timeouts += 1
            else:
                self._wrongCodes += 1

    @property
    def succeeded(self):
        return self._succeeded

    @property
    def failed(self):
        return self.wrongCodes + self.unknownExceptions + self.timeouts

    @property
    def wrongCodes(self):
        return self._wrongCodes

    @property
    def unknownExceptions(self):
        return self._unknownExceptions

    @property
    def timeouts(self):
        return self._timeouts

    @property
    def timeout_duration(self):
        return self._timeout_duration

    @property
    def totaltime(self):
        return self._totaltime

    @property
    def totaltime_ms(self):
        return self._totaltime * 1000

    @property
    def resultsize(self):
        return self._resultsize

    @property
    def penalizedtime(self):
        return self._penalizedtime

    @property
    def penalizedtime_ms(self):
        return self._penalizedtime * 1000

    @property
    def queryID(self):
        return self._queryID

    @property
    def qps(self):
        return self.succeeded / self.totaltime
