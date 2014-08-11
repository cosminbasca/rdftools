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
from rdftools.log import get_logger
from rdftools.tools import Lubm, RaptorRdf
from rdftools.util import working_directory

__author__ = 'basca'


class DataGenerator(object):
    __metaclass__ = ABCMeta

    def __init__(self, output_path, sites, **kwargs):
        self._output_path = output_path
        self._num_sites = sites
        self._log = get_logger(owner=self)

    @property
    def num_sites(self):
        return self._num_sites

    @property
    def output_path(self):
        return self._output_path

    @abstractmethod
    def _prepare(self, **kwargs):
        pass

    @abstractmethod
    def _generate(self, **kwargs):
        pass

    def __call__(self, **kwargs):
        self._log.info('preparing ... ')
        self._prepare(**kwargs)
        self._log.info('generating ... ')
        self._generate(**kwargs)
        self._log.info('complete')


class LubmGenerator(DataGenerator):
    __metaclass__ = ABCMeta

    def __init__(self, output_path, sites, universities=10, index=0, clean=True, **kwargs):
        super(LubmGenerator, self).__init__(output_path, sites, **kwargs)
        self._universities = universities
        self._index = index
        self._clean = clean

    def _prepare(self, **kwargs):
        # prepare the lubm data
        lubm_generator = Lubm()
        self._log.info('prepare LUBM for {0} universities'.format(self._universities))
        lubm_generator(self._universities, index=self._index)

    def _generate(self, **kwargs):
        universities_rdf = [f for f in os.listdir(self.output_path) if os.path.isfile(f) and f.startswith('University')]
        self._create_distribution(universities_rdf, **kwargs)

    def site_path(self, site_num):
        return os.path.join(self.output_path, 'site_%s.nt' % site_num)

    @abstractmethod
    def _create_distribution(self, universities_rdf, **kwargs):
        pass

    def __call__(self, **kwargs):
        self._log.info('generating data [working directory = {0}]'.format(sh.pwd().strip()))
        super(LubmGenerator, self).__call__(**kwargs)
        [os.remove(os.path.join(self.output_path, 'University%s.nt' % i)) for i in xrange(self._universities)]


