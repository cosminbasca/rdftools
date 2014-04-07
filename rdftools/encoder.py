import io
from util import log_time
import sys
from cybloom import ScalableBloomFilter
from random import randint
from rdftools.rdfparse import rdf_stream, MB, KB, parse
from rdftools.gcityhash import city64

__author__ = 'basca'

FP_ERR_RATE = 0.5
MIL = 1000000
INIT_CAPACITY_HIGH = 100 * MIL  # 100 million
INIT_CAPACITY_MED = 10 * MIL  # 10 million
INIT_CAPACITY_LOW = 10000  # 10K
INIT_CAPACITY_XTRA_LOW = 1000  # 10K


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


@log_time(None)
def encode_rdf(source_file, capacity_triples=INIT_CAPACITY_MED):
    class Visitor(object):
        def __init__(self):
            self.keys = ScalableBloomFilter(capacity_triples, FP_ERR_RATE)
            self.key_literals = ScalableBloomFilter(capacity_triples, FP_ERR_RATE)
            self.t_count = 0
            self.out_file = io.open('%s.ent' % source_file, 'wb+', buffering=512 * KB)

            # loop optimisations
            self.write = self.out_file.write

        def __del__(self):
            self.out_file.close()

        def __call__(self, s, p, o, c):
            if self.t_count % 50000 == 0 and self.t_count > 0:
                print '[processed %d triples]' % self.t_count
                sys.stdout.flush()

            self.write('%s %s %s\n' % (
                encode(self.keys, self.key_literals, s),
                encode(self.keys, self.key_literals, p),
                encode(self.keys, self.key_literals, o)
            ))

            self.t_count += 1

    visitor = Visitor()
    parse(source_file, visitor)


"""
parallel impl:

PARSER + ENCODER components they read in files + output (filename, {k:v, k:v, ...}) tuples

one WRITER component with the 2 SBF, checking for collisions! + WRITE to filename
"""