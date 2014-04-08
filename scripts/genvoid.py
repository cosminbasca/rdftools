#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
from pprint import pformat
from rdftools.__version__ import str_version
from rdftools.tools import Void


def main():
    parser = argparse.ArgumentParser(description='generate void statistics for RDF files')

    parser.add_argument('source', metavar='SOURCE', type=str,
                        help='the source file or location (of files) to be converted')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using version %s' % str_version
    else:
        void_generator = Void(args.source)
        stats = void_generator()
        print '-----------------------------------------------------------------------------'
        print 'Collected Statistics (VoID)'
        print pformat(stats)
        print '-----------------------------------------------------------------------------'


if __name__ == '__main__':
    main()