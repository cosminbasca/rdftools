from rdftools.util import log_time
from rdftools.rdfparse import parse
from abc import ABCMeta, abstractmethod

__author__ = 'basca'


class RdfTool(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def _run(self, *args, **kwargs):
        pass

    # @log_time(None)
    def __call__(self, *args, **kwargs):
        return self._run(*args, **kwargs)


class ParserVisitorTool(RdfTool):
    __metaclass__ = ABCMeta

    def __init__(self, source_file, **kwargs):
        self.source_file = source_file

    @abstractmethod
    def on_visit(self, s, p, o, c):
        pass

    @abstractmethod
    def get_results(self, *args, **kwargs):
        return None

    # @log_time(None)
    def _run(self, *args, **kwargs):
        parse(self.source_file, self.on_visit)
        return self.get_results(*args, **kwargs)