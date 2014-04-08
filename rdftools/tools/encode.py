import io
import sys
from cybloom import ScalableBloomFilter
from random import randint
from rdftools.gcityhash import city64
from rdftools.raptorutil import KB
from rdftools.tools.base import ParserVisitorTool
from void import INIT_CAPACITY_MED, FP_ERR_RATE, MIL

__author__ = 'basca'

def encode(keys, key_literals, value):
    _key = city64(value)
    while True:
        key = '%d' % _key
        mapping = '%s->%s' % (key, value)
        if not keys.check(key):
            # no collision
            keys.add(key)
            key_literals.add(mapping)
            return key
        else:
            # a possible collision
            if not key_literals.check(mapping):
                print '[collision detected]'
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
            print '[processed %d triples]' % self.t_count
            sys.stdout.flush()

        self.write('%s %s %s\n' % (
            encode(self.keys, self.key_literals, s),
            encode(self.keys, self.key_literals, p),
            encode(self.keys, self.key_literals, o)
        ))

        self.t_count += 1

    def get_results(self):
        return True
