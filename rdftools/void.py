from cybloom import ScalableBloomFilter
from converter import rdf_stream, MB

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
def get_void_stats(source_file, initial_capacity = INIT_CAPACITY_HIGH):
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

    for rdf_statement in rdf_stream(source_file, buffer_size=16*MB):
        s,p,o = rdf_statement[:3]

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
