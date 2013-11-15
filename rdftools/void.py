from collections import defaultdict
import os
from pprint import pformat
from cybloom import ScalableBloomFilter, Sketch
from converter import rdf_stream, MB
from util import log_time
import sys

__author__ = 'basca'

FP_ERR_RATE = 0.001
INIT_CAPACITY_HIGH = 100000000  # 100 million
INIT_CAPACITY_MED = 10000000  # 10 million
INIT_CAPACITY_LOW = 10000   #
#-----------------------------------------------------------------------------------------------------------------------
#
# analyze void from file, returns a VoID dict stats
#
#-----------------------------------------------------------------------------------------------------------------------

examples = '''

CAN BE APPROXIMATES

:DBpedia a void:Dataset;
    void:triples 1000000000;
    void:entities 3400000;
    .


void:Linkset is a subclass of void:Dataset,
:DBpedia2DBLP a void:Linkset;
    void:target :DBpedia;
    void:target :DBLP;
    void:linkPredicate owl:sameAs;
    void:triples 10000;
    .



Class- and property-based partitions
:DBpedia a void:Dataset;
    void:classPartition [
        void:class foaf:Person;
        void:entities 312000;
    ];
    void:propertyPartition [
        void:property foaf:name;
        void:triples 312000;
    ];
    .
'''

class UniqueCounter(object):
    def __init__(self, init_capacity, err_rate = FP_ERR_RATE):
        self.unique_count = 0
        self.sbf = ScalableBloomFilter(init_capacity, err_rate)

    def add(self, item):
        if not self.sbf.add(item):
            self.unique_count +=1

class PartitionCounter(object):
    def __init__(self, init_capacity, err_rate = FP_ERR_RATE):
        self.unique_counts = defaultdict(lambda : UniqueCounter(init_capacity, err_rate))

    def add(self, key, value):
        self.unique_counts[key].add(value)

    def counts(self):
        return dict([(k, uc.unique_count) for k, uc in self.unique_counts.items()])


@log_time(None)
def get_void_stats_fragment(source_file):
    sbf_classes     = UniqueCounter(INIT_CAPACITY_LOW, FP_ERR_RATE)
    sbf_properties  = UniqueCounter(INIT_CAPACITY_LOW, FP_ERR_RATE)
    sbf_subjects    = UniqueCounter(INIT_CAPACITY_HIGH, FP_ERR_RATE)
    sbf_objects     = UniqueCounter(INIT_CAPACITY_HIGH, FP_ERR_RATE)

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

    part_classes    = PartitionCounter(INIT_CAPACITY_HIGH, FP_ERR_RATE)
    part_properties = PartitionCounter(INIT_CAPACITY_HIGH, FP_ERR_RATE)

    t_count = 0
    for t_count,rdf_statement in enumerate(rdf_stream(source_file, buffer_size=128*MB)):
        s,p,o = rdf_statement[:3]
        if t_count % 10000 == 0 and t_count > 0:
            print '[processed %d triples]'%t_count
            sys.stdout.flush()

        sbf_subjects.add(s)
        sbf_properties.add(p)
        sbf_objects.add(o)
        if p=='http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
            sbf_classes.add(o)
            part_classes.add(o, '%s %s'%(s,p))
        part_properties.add(p, '%s %s'%(s,o))

    stats['triples']                = t_count
    stats['properties']             = sbf_properties.unique_count
    stats['classes']                = sbf_classes.unique_count
    stats['subjects']               = sbf_subjects.unique_count
    stats['objects']                = sbf_objects.unique_count
    stats['partition_classes']      = part_classes.counts()
    stats['partition_properties']   = part_properties.counts()

    print 'stats -> %s'%pformat(stats)
