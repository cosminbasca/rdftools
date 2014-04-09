"""
an Lubm data generator that follows several data modes of distribution

data mode 1: each uni is distributed to one host
data mode 2: horizontal partitioning of all data (based on stars)
data mode 3: randoly distribute a seed of resources to hosts, propagate from that point on (keep seed specific stuff on the same host)
data mode 4: choose a distribution (normal) for a university and distribute the data in the university to some machines given that uni
see substitution smapling
"""
import os
import sh
from abc import ABCMeta, abstractmethod
from tempfile import mkdtemp
from rdftools.tools import Lubm
from rdftools.util import working_directory

__author__ = 'basca'


class DataGenerator(object):
    __metaclass__ = ABCMeta

    def __init__(self, output_path, **kwargs):
        self._output_path = output_path

    @property
    def output_path(self):
        return self._output_path

    @abstractmethod
    def _prepare(self, *args, **kwargs):
        pass

    @abstractmethod
    def _generate(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        self._prepare(*args, **kwargs)
        self._generate(*args, **kwargs)


class LubmGenerator(DataGenerator):
    __metaclass__ = ABCMeta

    def __init__(self, output_path, temp_folder=None, universities=10, index=0, **kwargs):
        super(LubmGenerator, self).__init__(output_path, **kwargs)
        self.temp_folder = temp_folder if temp_folder else mkdtemp()
        self._universities = universities
        self._index = index

    def _prepare(self, *args, **kwargs):
        # prepare the lubm data
        lubm_generator = Lubm()
        print 'generate the LUBM data ... '
        lubm_generator(self._universities, self._index)


    def _generate(self, *args, **kwargs):
        universities_rdf = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.owl')]
        print 'universities = %s' % universities_rdf
        self._create_distribution(universities_rdf)

    @abstractmethod
    def _create_distribution(self, universities_rdf):
        pass

    def __call__(self, *args, **kwargs):
        with working_directory(self.temp_folder):
            print 'generating data [working directory = %s]' % (sh.pwd())
            super(LubmGenerator, self).__call__(*args, **kwargs)
            print 'cleanup LUBM files ... '
            sh.rm('*.owl')
            print 'distribution generated in [%s]' % (sh.pwd())

