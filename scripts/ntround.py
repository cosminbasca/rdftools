#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
from rdftools.__version__ import str_version
from rdftools.tools import NtFloatRounder


def main():
    parser = argparse.ArgumentParser(
        description='rounds ntriple files in a folder, (rounds the floating point literals)')

    parser.add_argument('path', metavar='PATH', type=str,
                        help='location of the indexes')

    parser.add_argument('--prefix', dest='prefix', action='store', type=str, default='rounded',
                        help='the prefix used for files that are transformed, cannot be the enpty string!')
    parser.add_argument('--precision', dest='precision', action='store', type=long, default=0,
                        help='the precision to round to, if 0, floating point numbers are rounded to long')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using rdftools version %s' % str_version
    else:
        rounder = NtFloatRounder()
        rounder(args.path, prefix=args.prefix, precision=args.precision)
        print 'done'


if __name__ == '__main__':
    main()