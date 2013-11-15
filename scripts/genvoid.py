#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
#from multiprocessing import Pool
from rdftools.__version__ import str_version
from rdftools.void import *


def main():
    """
    """
    parser = argparse.ArgumentParser(description='generate void statistics for RDF files')

    parser.add_argument('source', metavar='SOURCE', type=str,
                       help='the source file or location (of files) to be converted')
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