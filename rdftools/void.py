from collections import defaultdict
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

@log_time(None)
def get_void_stats_fragment(source_file, initial_capacity = INIT_CAPACITY_HIGH):
    sbf_entities = ScalableBloomFilter(initial_capacity, FP_ERR_RATE)
    sbf_classes = ScalableBloomFilter(INIT_CAPACITY_LOW, FP_ERR_RATE)
    sbf_properties = ScalableBloomFilter(INIT_CAPACITY_LOW, FP_ERR_RATE)
    sbf_subjects = ScalableBloomFilter(INIT_CAPACITY_HIGH, FP_ERR_RATE)
    sbf_objects = ScalableBloomFilter(INIT_CAPACITY_HIGH, FP_ERR_RATE)

    stats = {
        'properties'        : 0,
        'triples'           : 0,
        'entities'          : 0,
        'distinct_objects'  : 0,
        'distinct_subjects' : 0,
        'classes'           : 0,
        'doc_path'          : source_file,
    }

    #class_partitions = defaultdict(lambda : ScalableBloomFilter(INIT_CAPACITY_MED, FP_ERR_RATE))
    #property_partitions = defaultdict(lambda : ScalableBloomFilter(INIT_CAPACITY_MED, FP_ERR_RATE))

    for i,rdf_statement in enumerate(rdf_stream(source_file, buffer_size=128*MB)):
        s,p,o = rdf_statement[:3]
        if i % 100000 == 0 and i > 0:
            print '[processed %d triples]'%i
            sys.stdout.flush()

        stats['triples'] += 1
        if not sbf_subjects.check(s):
            sbf_subjects.add(s)
            stats['distinct_subjects'] += 1
        if not sbf_properties.check(p):
            sbf_properties.add(p)
            stats['properties'] += 1
        if not sbf_objects.check(o):
            sbf_objects.add(o)
            stats['distinct_objects'] += 1
        # classes
        if p=='http://www.w3.org/1999/02/22-rdf-syntax-ns#type' and \
            not sbf_classes.check(o):
            sbf_classes.add(o)
            stats['classes'] += 1
        # partitions

    print 'stats -> ',stats
