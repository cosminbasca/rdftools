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
from rdftools.tools import Lubm, RaptorRdf
from rdftools.util import working_directory

__author__ = 'basca'


class DataGenerator(object):
    __metaclass__ = ABCMeta

    def __init__(self, output_path, sites, **kwargs):
        self._output_path = output_path
        self._sites = sites

    @property
    def sites(self):
        return self._sites

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
        print 'prepare ... '
        self._prepare(*args, **kwargs)
        print 'generate ... '
        self._generate(*args, **kwargs)
        print 'done'


class LubmGenerator(DataGenerator):
    __metaclass__ = ABCMeta

    def __init__(self, output_path, sites, universities=10, index=0, clean=True, **kwargs):
        super(LubmGenerator, self).__init__(output_path, sites, **kwargs)
        self._universities = universities
        self._index = index
        self._clean = clean

    def _prepare(self, *args, **kwargs):
        # prepare the lubm data
        lubm_generator = Lubm()
        print 'generate the LUBM data ... '
        lubm_generator(self._universities, self._index)

    def _generate(self, *args, **kwargs):
        universities_rdf = [f for f in os.listdir(self.output_path) if os.path.isfile(f) and f.startswith('University')]
        print 'universities = %s' % universities_rdf
        self._create_distribution(universities_rdf)

    def site_path(self, site_num):
        return os.path.join(self.output_path, 'site_%s.nt' % site_num)

    @abstractmethod
    def _create_distribution(self, universities_rdf):
        pass

    def __call__(self, *args, **kwargs):
        print 'generating data [working directory = %s]' % (sh.pwd().strip())
        super(LubmGenerator, self).__call__(*args, **kwargs)
        [os.remove(os.path.join(self.output_path, 'University%s.nt' % i)) for i in xrange(self._universities)]


