from rdftools.util import log_time
from rdftools.rdfparse import parse
from abc import ABCMeta, abstractmethod

__author__ = 'basca'

class RdfTool(object):
    __metaclass__ = ABCMeta


class ParserVisitorTool(RdfTool):
    __metaclass__ = ABCMeta

    def __init__(self, source_file, **kwargs):
        self.source_file = source_file

    @abstractmethod
    def __call__(self, s, p, o, c):
        pass

    @abstractmethod
    def get_results(self):
        return None

    @log_time(None)
    def run(self):
        parse(self.source_file, self)
        return self.get_results()