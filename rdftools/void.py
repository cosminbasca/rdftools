from collections import defaultdict
import io
import os
from cybloom import ScalableBloomFilter, Sketch
from py4j.java_gateway import JavaGateway
from converter import rdf_stream, MB, KB, parse
from rdftools import BUNDLED_NXPARSER_JAR
from util import log_time
import sys
from yaml import dump

__author__ = 'basca'

FP_ERR_RATE = 0.5
MIL = 1000000
INIT_CAPACITY_HIGH = 100* MIL   # 100 million
INIT_CAPACITY_MED = 10* MIL     # 10 million
INIT_CAPACITY_LOW = 10000       # 10K
INIT_CAPACITY_XTRA_LOW = 1000   # 10K
#-----------------------------------------------------------------------------------------------------------------------
#
# analyze void from file, returns a VoID dict stats
#
#-----------------------------------------------------------------------------------------------------------------------
class UniqueCounter(object):
    def __init__(self, init_capacity, err_rate = FP_ERR_RATE):
        self.unique_count = 0
        self.sbf = ScalableBloomFilter(init_capacity, err_rate)
        self._add = self.sbf.add

    def add(self, item):
        if not self._add(item):
            self.unique_count +=1

#class PartitionCounter(object):
#    def __init__(self, init_capacity, err_rate = FP_ERR_RATE):
#        self.unique_counts = defaultdict(lambda : UniqueCounter(init_capacity, err_rate))
#
#    def add(self, key, value):
#        self.unique_counts[key].add(value)
#
#    def counts(self):
#        return dict([(k, uc.unique_count) for k, uc in self.unique_counts.items()])
#
#    def __len__(self):
#        return len(self.unique_counts)

class PartitionCounter(object):
    def __init__(self, init_capacity, err_rate = FP_ERR_RATE):
        self.unique_counts = defaultdict(lambda : UniqueCounter(init_capacity, err_rate))

    def add(self, key, value):
        self.unique_counts[key].add(value)

    def counts(self):
        return dict([(k, uc.unique_count) for k, uc in self.unique_counts.items()])

    def __len__(self):
        return len(self.unique_counts)


@log_time(None)
def get_void_stats_fragment(source_file, capacity_triples=INIT_CAPACITY_MED):
    class Visitor(object):
        def __init__(self):
            self.sbf_subjects        = UniqueCounter(capacity_triples, FP_ERR_RATE)
            self.sbf_objects         = UniqueCounter(capacity_triples, FP_ERR_RATE)
            self.part_classes        = PartitionCounter(capacity_triples, FP_ERR_RATE)
            self.part_properties     = PartitionCounter(capacity_triples, FP_ERR_RATE)
            self.t_count             = 0

            # loop optimisations
            self.sbf_subjects_add    = self.sbf_subjects.add
            self.sbf_objects_add     = self.sbf_objects.add
            self.part_classes_add    = self.part_classes.add
            self.part_properties_add = self.part_properties.add

            #TODO: some of these stats require a min sketch counter - not unique - implement this later...
            self.stats = {
                'properties'            : 0,
                'triples'               : 0,
                'objects'               : 0,
                'subjects'              : 0,
                'classes'               : 0,
                'doc_path'              : os.path.abspath(source_file),
                'partition_classes'     : None,
                'partition_properties'  : None,
            }

        def __call__(self, s,p,o,c):
            if self.t_count % 50000 == 0 and self.t_count > 0:
                print '[processed %d triples]'%self.t_count
                sys.stdout.flush()

            self.sbf_subjects_add(s)
            self.sbf_objects_add(o)
            if p=='http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                self.part_classes_add(o, '%s %s'%(s,p))
            self.part_properties_add(p, '%s %s'%(s,o))
            self.t_count += 1

        def get_stats(self):
            self.stats['triples']                = self.t_count
            self.stats['properties']             = len(self.part_properties)
            self.stats['classes']                = len(self.part_classes)
            self.stats['subjects']               = self.sbf_subjects.unique_count
            self.stats['objects']                = self.sbf_objects.unique_count
            self.stats['partition_classes']      = self.part_classes.counts()
            self.stats['partition_properties']   = self.part_properties.counts()

            with io.open('%s.yaml'%source_file, 'w+') as OUT:
                dump(self.stats, OUT)

            return self.stats

    visitor = Visitor()
    parse(source_file, visitor)
    return visitor.get_stats()