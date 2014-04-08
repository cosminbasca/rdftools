#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
from pprint import pformat
from rdftools.__version__ import str_version
from rdftools.tools import RaptorRdf


def main():
    parser = argparse.ArgumentParser(description='rdf converter, based on libraptor2')

    parser.add_argument('source', metavar='SOURCE', type=str,
                        help='the source file or location (of files) to be converted')
    parser.add_argument('--clear', dest='clear', action='store_true',
                        help='clear the original files (delete) - this action is permanent, use with caution!')
    parser.add_argument('--dst_format', dest='dst_format', action='store', type=str, default='ntriples',
                        help='the destination format to convert to. Supported parsers: %s. Supported serializers %s.' % (
                            pformat(RaptorRdf.parsers), pformat(RaptorRdf.serializers)))
    parser.add_argument('--buffer_size', dest='buffer_size', action='store', type=long, default=64,
                        help='the buffer size in Mb of the input buffer (the parser will only parse XX Mb at a time)')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using version %s' % str_version
    else:
        rdf_converter = RaptorRdf()
        rdf_converter(args.source, destination_format=args.dst_format, buffer_size=args.buffer_size,
                      clear=args.clear)
        print 'done'


if __name__ == '__main__':
    main()