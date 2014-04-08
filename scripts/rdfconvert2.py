#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
from rdftools.__version__ import str_version
from rdftools.tools import *


def main():
    parser = argparse.ArgumentParser(description='rdf converter (2), makes use of rdf2rdf bundled - requires java')

    parser.add_argument('source', metavar='SOURCE', type=str,
                        help='the source file or location (of files) to be converted')
    parser.add_argument('--clear', dest='clear', action='store_true',
                        help='clear the original files (delete) - this action is permanent, use with caution!')
    parser.add_argument('--dst_format', dest='dst_format', action='store', type=str, default='ntriples',
                        help='the destination format to convert to')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using rdftools version %s' % str_version
    else:
        rdf_converter = Rdf2Rdf()
        rdf_converter(args.source, args.dst_format, clear_source=args.clear)
        print 'done'


if __name__ == '__main__':
    main()