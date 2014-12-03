#
# author: Cosmin Basca
#
# Copyright 2010 University of Zurich
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from collections import defaultdict
from base import LubmGenerator, UniTriplesDistribution
from rdftools.gcityhash import city64
from rdftools.log import logger
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

PERMUTATIONS = ('s', 'p', 'o', 'sp', 'so', 'po', 'spo')

class HashPartitioner(ParserVisitorTool):
    def __init__(self, source_file, num_sites=0, permutation=None, **kwargs):
        super(HashPartitioner, self).__init__(source_file, **kwargs)
        if num_sites == 0:
            raise ValueError('num_partitions cannot be 0')
        self.num_sites = num_sites
        if permutation not in PERMUTATIONS:
            raise ValueError('permutaion must be one of {0}, instead got {1}'.format(PERMUTATIONS, permutation))
        self._permutation = permutation
        self.site_index = []

    def on_visit(self, s, p, o, c):
        site_idx = city64(_part((s, p, o), self._permutation)) % self.num_sites
        self.site_index.append(site_idx)

    def get_results(self, *args, **kwargs):
        return self.site_index


"""
distribution process:

1) horizontal partitioning of all data (based on stars)
"""
class LubmHorizontal(LubmGenerator):
    def __init__(self, output_path, sites, permutation='s', **kwargs):
        super(LubmHorizontal, self).__init__(output_path, sites, **kwargs)
        self._permutation = permutation

    @property
    def _distributor_type(self):
        return UniHorizontal

    def _distributor_kwargs(self, uni_id, uni_rdf):
        return dict(permutation=self._permutation)


class UniHorizontal(UniTriplesDistribution):
    def _distribute_triples(self, triples, permutation='s'):
        logger.info('[distributing] university %s by %s', self.uni_name, permutation)
        site_index = HashPartitioner(self.uni_rdf, num_sites=self.num_sites, permutation=permutation)()

        site_triples = defaultdict(list)

        sites = [0 for i in xrange(self.num_sites)]
        for i, triple in enumerate(triples):
            sites[site_index[i]] += 1
            site_triples[site_index[i]].append(triple)
        logger.info('university %s total triples = %s, distribution = %s', self.uni_rdf, len(triples), sites)

        return site_triples