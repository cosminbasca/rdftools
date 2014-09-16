from collections import defaultdict
from base import LubmGenerator, UniTriplesDistribution
import numpy as np
from log import logger
import io
import sh

__author__ = 'basca'

DISTRIBUTIONS = {
    # one uni to 3 sites
    # '3S': np.array([1.0,
    # 2.0,
    #                   1.0]) / 4.0,

    '3S': np.array([3.0,
                    10.0,
                    3.0]) / 16.0,

    # one uni to 5 sites
    '5S': np.array([1.0,
                    3.0,
                    8.0,
                    3.0,
                    1.0]) / 16.0,

    # one uni to 7 sites
    '7S': np.array([1.0,
                    3.0,
                    12.0,
                    32.0,
                    12.0,
                    3.0,
                    1.0]) / 64.0,

}

is_valid_distribution = lambda distro: np.sum(distro) == 1.0

"""
distribution process:
1) choose a distribution (normal) for a university
2) distribute the data of the university to some machines given that uni
obs: see substitution smapling
"""


class LubmUni2Many(LubmGenerator):

    def __init__(self, output_path, sites, universities=10, index=0, clean=True, pdist = None, **kwargs):
        super(LubmUni2Many, self).__init__(output_path, sites, universities=universities, index=index, clean=clean,
                                           **kwargs)
        if not isinstance(pdist, np.ndarray):
            raise ValueError('pdist must be a numpy ndarray')
        if not is_valid_distribution(pdist):
            raise ValueError('pdist is not valid, all values must sum up to 1. SUM({0}) = {1}'.format(
                pdist, np.sum(pdist)))

        self._pdist = pdist
        self._sorted_pdist = np.sort(self._pdist)
        num_extra_sites = len(self._sorted_pdist) - 1

        base_sites = np.random.random_integers(0, self._num_sites - 1, self.num_universities)
        print 'base sites = ', base_sites

        sites = np.arange(self._num_sites)

        self._uni_site_distros = [
            # get the disrtribution of sites for that uni, base_sites[i] = the base university
            [base_sites[i]] + list(
                np.random.choice(sites[sites != base_sites[i]], num_extra_sites, replace=False))
            for i in xrange(self.num_universities)
        ]

    @property
    def _distributor_type(self):
        return Uni2Many

    def _distributor_kwargs(self, uni_id, uni_rdf):
        return dict(uni_site_distro=self._uni_site_distros[uni_id], sorted_pdist=self._sorted_pdist)


class Uni2Many(UniTriplesDistribution):
    def _distribute_triples(self, triples, uni_site_distro=None, sorted_pdist=None):
        if not isinstance(uni_site_distro, list) and len(uni_site_distro) > 0:
            raise ValueError('uni_site_distro must be a non empty List')
        if not isinstance(sorted_pdist, np.ndarray):
            raise ValueError('sorted_p_distro must be a Numpy ndarray')

        num_triples = len(triples)
        logger.info('[distributing] university %s to sites: %s, with %s triples', self.uni_name, uni_site_distro,
                    num_triples)
        site_index = np.random.choice(uni_site_distro, num_triples, p=sorted_pdist)

        site_triples = defaultdict(list)
        for j, triple in enumerate(triples):
            site_triples[site_index[j]].append(triple)

        return site_triples