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