from base import LubmGenerator, UniTriplesDistribution
import numpy as np
import io

__author__ = 'basca'

"""
distribution process:

1) each uni is distributed to one host
"""


class LubmUni2One(LubmGenerator):
    def __init__(self, output_path, sites, universities=10, index=0, clean=True, **kwargs):
        super(LubmUni2One, self).__init__(output_path, sites, universities=universities, index=index, clean=clean,
                                          **kwargs)
        self._sites_index = np.random.random_integers(0, self._num_sites - 1, self.num_universities)

    @property
    def _distributor_type(self):
        return Uni2One

    def _distributor_kwargs(self, uni_id, uni_rdf):
        return dict(uni_site=self._sites_index[uni_id])


class Uni2One(UniTriplesDistribution):
    def _distribute_triples(self, triples, uni_site=None):
        if uni_site is None:
            raise ValueError('uni_site cannot be None')
        return {uni_site: triples}