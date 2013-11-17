from collections import defaultdict
import io
import os
from cybloom import ScalableBloomFilter, Sketch
from py4j.java_gateway import JavaGateway
from converter import rdf_stream, MB, KB
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

    sbf_subjects        = UniqueCounter(capacity_triples, FP_ERR_RATE)
    sbf_objects         = UniqueCounter(capacity_triples, FP_ERR_RATE)
    part_classes        = PartitionCounter(capacity_triples, FP_ERR_RATE)
    part_properties     = PartitionCounter(capacity_triples, FP_ERR_RATE)
    t_count             = 0

    # loop optimisations
    sbf_subjects_add    = sbf_subjects.add
    sbf_objects_add     = sbf_objects.add
    part_classes_add    = part_classes.add
    part_properties_add = part_properties.add

    #TODO: some of these stats require a min sketch counter - not unique - implement this later...
    stats = {
        'properties'            : 0,
        'triples'               : 0,
        'objects'               : 0,
        'subjects'              : 0,
        'classes'               : 0,
        'doc_path'              : os.path.abspath(source_file),
        'partition_classes'     : None,
        'partition_properties'  : None,
    }

    # -----------------------------------------------------------------------------
    # using NX parser
    #gateway = JavaGateway.launch_gateway(classpath='.:%s'%BUNDLED_NXPARSER_JAR)
    #jvm = gateway.jvm
    #source_is = jvm.java.io.FileInputStream(source_file)
    #nxparser = jvm.org.semanticweb.yars.nx.parser.NxParser(source_is)
    #while nxparser.hasNext():
    #    node = nxparser.next()
    #    s = str(node[0].toString())
    #    p = str(node[1].toString())
    #    o = str(node[2].toString())
    # too slow when called from python ...
    # -----------------------------------------------------------------------------
    # using the RAPTOR parser
    for s,p,o,c in rdf_stream(source_file, buffer_size=64*MB):
    # -----------------------------------------------------------------------------

        if t_count % 50000 == 0 and t_count > 0:
            print '[processed %d triples]'%t_count
            sys.stdout.flush()

        sbf_subjects_add(s)
        sbf_objects_add(o)
        if p=='http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
            part_classes_add(o, '%s %s'%(s,p))
        part_properties_add(p, '%s %s'%(s,o))
        t_count += 1

    stats['triples']                = t_count
    stats['properties']             = len(part_properties)
    stats['classes']                = len(part_classes)
    stats['subjects']               = sbf_subjects.unique_count
    stats['objects']                = sbf_objects.unique_count
    stats['partition_classes']      = part_classes.counts()
    stats['partition_properties']   = part_properties.counts()

    with io.open('%s.yaml'%source_file, 'w+') as OUT:
        dump(stats, OUT)

    return stats
