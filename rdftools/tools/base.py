from rdftools.log import get_logger
from rdftools.rdfparse import parse
from abc import ABCMeta, abstractmethod

__author__ = 'basca'


class RdfTool(object):
    __metaclass__ = ABCMeta

    def __init__(self, *args, **kwargs):
        self._log = get_logger(owner=self)

    @abstractmethod
    def _run(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return self._run(*args, **kwargs)


class ParserVisitorTool(RdfTool):
    __metaclass__ = ABCMeta

    def __init__(self, source_file, *args, **kwargs):
        super(ParserVisitorTool, self).__init__(*args, **kwargs)
        self.source_file = source_file

    @abstractmethod
    def on_visit(self, s, p, o, c):
        pass

    @abstractmethod
    def get_results(self, *args, **kwargs):
        return None

    def _run(self, *args, **kwargs):
        parse(self.source_file, self.on_visit)
        return self.get_results(*args, **kwargs)