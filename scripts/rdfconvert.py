#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
import time
import sys
import os
from multiprocessing import Pool
from rdftools import *
from rdftools.__version__ import str_version
from pprint import pformat

#-----------------------------------------------------------------------------------------------------------------------
#
# parallel processor
#
#-----------------------------------------------------------------------------------------------------------------------
def convert_files(files, dst_format, buffer_size):
    def job_finished(res):
        print '|',
        sys.stdout.flush()

    pool = Pool()
    for src in files:
        pool.apply_async(convert_chunked,(src, dst_format, buffer_size), callback = job_finished)

    pool.close()
    pool.join()

#-----------------------------------------------------------------------------------------------------------------------
#
# supported serializers and parsers
#
#-----------------------------------------------------------------------------------------------------------------------
parsers = [
    'rdfxml',
    'ntriples',
    'turtle',
    'trig',
    'guess',
    'rss-tag-soup',
    'rdfa',
    'nquads',
    'grddl'
]

serializers = [
    'rdfxml',
    'rdfxml-abbrev',
    'turtle',
    'ntriples',
    'rss-1.0',
    'dot',
    'html',
    'json',
    'atom',
    'nquads'
]


def main():
    """

    """
    parser = argparse.ArgumentParser(description='rdf converter, based on libraptor2')

    parser.add_argument('source', metavar='SOURCE', type=str,
                       help='the source file or location (of files) to be converted')
    parser.add_argument('--clear', dest='clear', action='store_true',
                       help='clear the original files (delete) - this action is permanent, use with caution!')
    parser.add_argument('--dst_format', dest='dst_format', action='store', type=str, default='ntriples',
                       help='the destination format to convert to. Supported parsers: %s. Supported serializers %s.'%(pformat(parsers), pformat(serializers)))
    parser.add_argument('--buffer_size', dest='buffer_size', action='store', type=long, default=160,
                       help='the buffer size in Mb of the input buffer (the parser will only parse XX Mb at a time)')
    parser.add_argument('--version', dest='version', action='store_true',
                       help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using version %s'%str_version
    else:
        t0      = time.time()
        files   = []
        src     = os.path.abspath(args.source)
        if  os.path.isdir(src):
            files = [os.path.join(src, f) for f in os.listdir(src) if supported(f) and get_parser_type(f) != args.dst_format]
        elif os.path.exists(src):
            files = [src]
        print 'To process : ',files
        if args.clear:
            print 'will remove original files after conversion'
        convert_files(files, args.dst_format, args.buffer_size * MB)

        if args.clear: [os.remove(f) for f in files]

        print 'Took %s seconds'%(str(time.time()-t0))


if __name__ == '__main__':
    main()