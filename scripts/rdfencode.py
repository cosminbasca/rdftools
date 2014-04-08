#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
from rdftools.__version__ import str_version
from rdftools.tools.encode import *


def main():
    parser = argparse.ArgumentParser(description='encode the RDF file(s)')

    parser.add_argument('source', metavar='SOURCE', type=str,
                        help='the source file or location (of files) to be encoded')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using version %s' % str_version
    else:
        encoder = RdfEncoder(args.source)
        encoder()
        print 'done'


if __name__ == '__main__':
    main()