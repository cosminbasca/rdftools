from collections import defaultdict
import io
import os
from pprint import pformat
from cybloom import ScalableBloomFilter
from converter import rdf_stream, MB, KB
from util import log_time
import sys
from yaml import load, dump

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

class PartitionCounter(object):
    def __init__(self, init_capacity, err_rate = FP_ERR_RATE):
        self.unique_counts = defaultdict(lambda : UniqueCounter(init_capacity, err_rate))

    def add(self, key, value):
        self.unique_counts[key].add(value)

    def counts(self):
        return dict([(k, uc.unique_count) for k, uc in self.unique_counts.items()])


@log_time(None)
def get_void_stats_fragment(source_file,
                            capacity_classes    = INIT_CAPACITY_XTRA_LOW,
                            capacity_properties = INIT_CAPACITY_XTRA_LOW,
                            capacity_triples    = INIT_CAPACITY_MED):

    sbf_classes     = UniqueCounter(capacity_classes, FP_ERR_RATE)
    sbf_properties  = UniqueCounter(capacity_properties, FP_ERR_RATE)
    sbf_subjects    = UniqueCounter(capacity_triples, FP_ERR_RATE)
    sbf_objects     = UniqueCounter(capacity_triples, FP_ERR_RATE)
    part_classes    = PartitionCounter(capacity_triples, FP_ERR_RATE)
    part_properties = PartitionCounter(capacity_triples, FP_ERR_RATE)
    t_count = 0

    # loop optimisations
    sbf_classes_add     = sbf_classes.add
    sbf_properties_add  = sbf_properties.add
    sbf_subjects_add    = sbf_subjects.add
    sbf_objects_add     = sbf_objects.add
    part_classes_add    = part_classes.add
    part_properties_add = part_properties.add

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


    for s,p,o,c in rdf_stream(source_file, buffer_size=16*MB):
        if t_count % 50000 == 0 and t_count > 0:
            print '[processed %d triples]'%t_count
            sys.stdout.flush()

        sbf_subjects_add(s)
        sbf_properties_add(p)
        sbf_objects_add(o)
        if p=='http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
            sbf_classes_add(o)
            part_classes_add(o, '%s %s'%(s,p))
        part_properties_add(p, '%s %s'%(s,o))
        t_count += 1

    stats['triples']                = t_count
    stats['properties']             = sbf_properties.unique_count
    stats['classes']                = sbf_classes.unique_count
    stats['subjects']               = sbf_subjects.unique_count
    stats['objects']                = sbf_objects.unique_count
    stats['partition_classes']      = part_classes.counts()
    stats['partition_properties']   = part_properties.counts()

    with io.open('%s.yaml'%source_file, 'w+') as OUT:
        dump(stats, OUT)

    return stats
