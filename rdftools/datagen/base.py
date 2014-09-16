from collections import OrderedDict
from multiprocessing import Pool
import os
import re
import io
import sh
from abc import ABCMeta, abstractmethod, abstractproperty
from tempfile import mkdtemp
from rdftools.log import get_logger, logger
from rdftools.tools import Lubm, RaptorRdf
from rdftools.util import working_directory
from natsort import natsorted

__author__ = 'basca'


class DataGenerator(object):
    __metaclass__ = ABCMeta

    def __init__(self, output_path, sites, **kwargs):
        self._output_path = os.path.abspath(output_path)
        if not os.path.isdir(self._output_path):
            raise ValueError('{0} not a valid path'.format(self._output_path))
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

    @property
    def num_universities(self):
        return self._universities

    def _prepare(self, **kwargs):
        # prepare the lubm data
        lubm_generator = Lubm(path=self._output_path)
        self._log.info('prepare LUBM for {0} universities'.format(self._universities))
        lubm_generator(self._universities, index=self._index)

    def _generate(self, **kwargs):
        uni_key = 'University'
        uni_ext = '.nt'
        get_uni_id = lambda uni_file: int(uni_file.replace(uni_key, '').replace(uni_ext, '').strip())

        universities_rdf = {
            get_uni_id(f): os.path.join(self.output_path, f)
            for f in os.listdir(self.output_path)
            if f.startswith(uni_key)
        }

        pool = Pool()
        for uni_id, uni_rdf in universities_rdf.iteritems():
            pool.apply_async(self.distributor(uni_id, uni_rdf),
                             kwds=self._distributor_kwargs(uni_id, uni_rdf))
        pool.close()
        pool.join()

        # concat files
        site_files = lambda site_id: re.findall(r'site_{0}_uni_[0-9]+\.nt'.format(site_id),
                                                ' '.join(os.listdir(self._output_path)))
        for site in xrange(self.num_sites):
            site_parts = site_files(site)
            logger.info('[site = %s] site file parts = %s', site, site_parts)

            with io.open(self.site_path(site), 'w+') as SITE:
                for spart in site_parts:
                    spart_file = os.path.join(self._output_path, spart)
                    with io.open(spart_file, 'r+') as SPART:
                        SITE.write(SPART.read())
                    sh.rm(spart_file)

    @abstractproperty
    def _distributor_type(self):
        return None

    @abstractmethod
    def _distributor_kwargs(self, uni_id, uni_rdf):
        return None

    def distributor(self, uni_id, uni_rdf):
        if not issubclass(self._distributor_type, UniTriplesDistribution):
            raise ValueError('distributor must be a UniTriplesDistribution')
        uni_distributor = self._distributor_type(uni_id, uni_rdf, self._num_sites, self._output_path)
        return uni_distributor

    def site_path(self, site_num):
        return os.path.join(self.output_path, 'site_%s.nt' % site_num)

    def __call__(self, **kwargs):
        self._log.info('generating data')
        super(LubmGenerator, self).__call__(**kwargs)
        if self._clean:
            [os.remove(os.path.join(self.output_path, 'University{0}.nt'.format(i))) for i in
             xrange(self._universities)]


class UniTriplesDistribution(object):
    __metaclass__ = ABCMeta

    def __init__(self, uni_id, university_rdf, sites, output_path):
        if not os.path.isfile(university_rdf):
            raise ValueError('university_rdf is not a valid file')
        self._uni_rdf = university_rdf
        self._num_sites = sites
        self._output_path = output_path
        self._uni_id = uni_id

    @property
    def uni_rdf(self):
        return self._uni_rdf

    @property
    def num_sites(self):
        return self._num_sites

    @property
    def output_path(self):
        return self._output_path

    @abstractmethod
    def _distribute_triples(self, triples, **kwargs):
        pass

    def site_part_path(self, site_num):
        return os.path.join(self.output_path, 'site_{0}_uni_{1}.nt'.format(site_num, self._uni_id))

    @property
    def uni_name(self):
        return os.path.splitext(os.path.split(self._uni_rdf)[-1])[0]

    def __call__(self, **kwargs):
        with open(self._uni_rdf, 'r') as UNI:
            triples = UNI.readlines()
            triples = self._distribute_triples(triples, **kwargs)
            if not isinstance(triples, dict):
                raise ValueError('triples must be a dictionary where the key is the number of the site')
            # write the triples to the site uni part
            for site_num, site_triples in triples.iteritems():
                with open(self.site_part_path(site_num), 'w+') as SITE_PART:
                    SITE_PART.write(''.join(site_triples))


