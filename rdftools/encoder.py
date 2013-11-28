from collections import defaultdict
import io
import os
from converter import rdf_stream, MB, KB, parse
from util import log_time
import sys
from yaml import dump
from cybloom import ScalableBloomFilter
from gcityhash import city64
from random import randint

__author__ = 'basca'

FP_ERR_RATE = 0.5
MIL = 1000000
INIT_CAPACITY_HIGH = 100* MIL   # 100 million
INIT_CAPACITY_MED = 10* MIL     # 10 million
INIT_CAPACITY_LOW = 10000       # 10K
INIT_CAPACITY_XTRA_LOW = 1000   # 10K

def encode(sbf_add, sbf_check, value):
    _key = city64(value)
    while True:
        _value = '%s%d'%(value, _key)
        if not sbf_check(_value):
            # no collision
            sbf_add(_value)
            return '%s'%_key
        else:
            # we have a collision
            print '[collision detected]'
            _key += randint(0, MIL)


@log_time(None)
def encode_rdf(source_file, capacity_triples=INIT_CAPACITY_MED):
    class Visitor(object):
        def __init__(self):
            self.rdf_literals        = ScalableBloomFilter(capacity_triples, FP_ERR_RATE)
            self.t_count             = 0
            self.out_file            = io.open('%s.ent'%source_file, 'wb+', buffering=512*KB)

            # loop optimisations
            self.rdf_literals_add    = self.rdf_literals.add
            self.rdf_literals_check  = self.rdf_literals.check
            self.write               = self.out_file.write

        def __del__(self):
            self.out_file.close()

        def __call__(self, s,p,o,c):
            if self.t_count % 50000 == 0 and self.t_count > 0:
                print '[processed %d triples]'%self.t_count
                sys.stdout.flush()

            self.write('%s %s %s\n'%(
                encode(self.rdf_literals_add, self.rdf_literals_check, s),
                encode(self.rdf_literals_add, self.rdf_literals_check, p),
                encode(self.rdf_literals_add, self.rdf_literals_check, o)
            ))

            self.t_count += 1

    visitor = Visitor()
    parse(source_file, visitor)