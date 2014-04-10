from collections import defaultdict
from base import LubmGenerator
from rdftools.gcityhash import city64
from rdftools.tools import ParserVisitorTool
import io

__author__ = 'basca'


def _part((s, p, o), perm):
    val = ''
    for c in perm:
        if c == 's':
            val += '%s' % s
        elif c == 'p':
            val += '%s' % p
        elif c == 'o':
            val += '%s' % o
    return val


class HashPartitioner(ParserVisitorTool):
    def __init__(self, source_file, num_sites=0, permutation=None, **kwargs):
        super(HashPartitioner, self).__init__(source_file, **kwargs)
        if num_sites == 0:
            raise ValueError('num_partitions cannot be 0')
        self.num_sites = num_sites
        self.permutations = permutation if permutation in ['s', 'p', 'o', 'sp', 'so', 'po', 'spo'] else ['s']
        self.site_index = []

    def on_visit(self, s, p, o, c):
        for permutation in self.permutations:
            site_idx = city64(_part((s, p, o), permutation)) % self.num_sites
            self.site_index.append(site_idx)

    def get_results(self, *args, **kwargs):
        return self.site_index


class LubmHorizontal(LubmGenerator):
    def __init__(self, output_path, sites, permutation='s', **kwargs):
        super(LubmHorizontal, self).__init__(output_path, sites, **kwargs)
        self._permutation = permutation

    def _create_distribution(self, universities_rdf):
        # open site files
        site_files = [io.open(self.site_path(i), mode='w+', buffering=1024 * 1024 * 16) for i in xrange(self.sites)]

        for uni_rdf in universities_rdf:
            print '[distributing] university %s by %s'%(uni_rdf, self._permutation)
            site_index = HashPartitioner(uni_rdf, num_sites=self.sites, permutation=self._permutation)()
            with io.open(uni_rdf, mode='r', buffering=1024 * 1024 * 16) as UNI:
                for i, triple in enumerate(UNI):
                    site = site_index[i]
                    site_files[site].write('%s\n'%triple)

        # close site files
        [site_rdf.close() for site_rdf in site_files]