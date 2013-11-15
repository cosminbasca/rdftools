#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
import time
import sys
from multiprocessing import Pool
from rdftools.__version__ import str_version
from rdftools.void import *

#-----------------------------------------------------------------------------------------------------------------------
#
# parallel LUBM generation
#
#-----------------------------------------------------------------------------------------------------------------------
#def generate_lubm(lubm_path, univ, index, seed, onto):
#    def job_finished(res):
#        print '|',
#        sys.stdout.flush()
#
#    max_unis = 10
#
#    pool = Pool()
#    for idx in xrange(index, univ+index, max_unis):
#        pool.apply_async(exec_lubm,(lubm_path, max_unis, idx, seed, onto), callback = job_finished)
#
#    pool.close()
#    pool.join()



def main():
    """
    """
    parser = argparse.ArgumentParser(description='generate void statistics for RDF files')

    parser.add_argument('source', metavar='SOURCE', type=str,
                       help='the source file or location (of files) to be converted')
    #parser.add_argument('--univ', dest='univ', action='store', type=long, default=1,
    #                   help='number of universities to generate')
    #parser.add_argument('--index', dest='index', action='store', type=long, default=0,
    #                   help='start university')
    #parser.add_argument('--seed', dest='seed', action='store', type=long, default=0,
    #                   help='the seed')
    #parser.add_argument('--ontology', dest='ontology', action='store', type=str, default=LUBM_ONTO,
    #                   help='the lubm ontology by default: %s'%LUBM_ONTO)
    parser.add_argument('--version', dest='version', action='store_true',
                       help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using version %s'%str_version
    else:
        get_void_stats_fragment(args.source)



PROFILE = False
#PROFILE = True

if __name__ == '__main__':
    if PROFILE:
        import cProfile
        command = """main()"""
        cProfile.runctx( command, globals(), locals())
    else:
        main()