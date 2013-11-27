from collections import defaultdict
import io
import os
from converter import rdf_stream, MB, KB, parse
from util import log_time
import sys
from yaml import dump
from cybloom import ScalableBloomFilter
from gcityhash import city64

__author__ = 'basca'

FP_ERR_RATE = 0.5
MIL = 1000000
INIT_CAPACITY_HIGH = 100* MIL   # 100 million
INIT_CAPACITY_MED = 10* MIL     # 10 million
INIT_CAPACITY_LOW = 10000       # 10K
INIT_CAPACITY_XTRA_LOW = 1000   # 10K


@log_time(None)
def encode_rdf(source_file, capacity_triples=INIT_CAPACITY_MED):
    class Visitor(object):
        def __init__(self):
            self.rdf_literals        = ScalableBloomFilter(INIT_CAPACITY_HIGH, FP_ERR_RATE)
            self.t_count             = 0
            #self.collisions          =

            # loop optimisations
            self.rdf_literals_add    = self.rdf_literals.add
            self.rdf_literals_check  = self.rdf_literals.check

        def __call__(self, s,p,o,c):
            if self.t_count % 50000 == 0 and self.t_count > 0:
                print '[processed %d triples]'%self.t_count
                sys.stdout.flush()

            if not self.rdf_literals_check(s):
                pass

            self.rdf_literals_add(s)
            self.rdf_literals_add(p)
            self.rdf_literals_add(o)

            self.t_count += 1

    visitor = Visitor()
    parse(source_file, visitor)