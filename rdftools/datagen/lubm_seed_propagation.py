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
from base import LubmGenerator

__author__ = 'basca'

"""
distribution process:

1) randoly distribute a seed of resources to hosts,
2) propagate from that point on (keep seed specific stuff on the same host)
"""
class LubmSeedPropagation(LubmGenerator):
    def _create_distribution(self, universities_rdf, **kwargs):
        #TODO: implement me!
        raise NotImplementedError