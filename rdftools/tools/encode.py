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
import io
from warnings import warn
from random import randint
from rdftools.gcityhash import city64
from rdftools.log import logger
from rdftools.raptorutil import KB
from rdftools.tools.base import ParserVisitorTool
from rdftools.tools.bloom import ScalableBloomFilter, check, add
from voidgen import INIT_CAPACITY_MED, FP_ERR_RATE, MIL

__author__ = 'basca'


def encode(keys, key_literals, value):
    _key = city64(value)
    while True:
        key = '%d' % _key
        mapping = '%s->%s' % (key, value)
        if not check(keys, key):
            # no collision
            add(keys, key)
            key_literals.add(mapping)
            return key
        else:
            # a possible collision
            if not key_literals.check(mapping):
                logger.warn('[collision detected]')
                _key += randint(0, MIL)
            else:
                return key


class RdfEncoder(ParserVisitorTool):
    def __init__(self, source_file, capacity_triples=INIT_CAPACITY_MED):
        super(RdfEncoder, self).__init__(source_file, capacity_triples=capacity_triples)

        self.keys = ScalableBloomFilter(capacity_triples, FP_ERR_RATE)
        self.key_literals = ScalableBloomFilter(capacity_triples, FP_ERR_RATE)
        self.t_count = 0
        self.out_file = io.open('%s.ent' % source_file, 'wb+', buffering=512 * KB)

        # loop optimisations
        self.write = self.out_file.write

    def __del__(self):
        self.out_file.close()

    def on_visit(self, s, p, o, c):
        if self.t_count % 50000 == 0 and self.t_count > 0:
            self._log.info('[processed {0} triples]'.format(self.t_count))

        self.write('%s %s %s\n' % (
            encode(self.keys, self.key_literals, s),
            encode(self.keys, self.key_literals, p),
            encode(self.keys, self.key_literals, o)
        ))

        self.t_count += 1

    def get_results(self):
        return True
