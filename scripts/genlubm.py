#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
from rdftools.__version__ import str_version
from rdftools.tools import Lubm


def main():
    parser = argparse.ArgumentParser(description='lubm dataset generator wrapper (bundled) - requires java')

    parser.add_argument('--univ', dest='univ', action='store', type=long, default=1,
                        help='number of universities to generate')
    parser.add_argument('--index', dest='index', action='store', type=long, default=0,
                        help='start university')
    parser.add_argument('--seed', dest='seed', action='store', type=long, default=0,
                        help='the seed')
    parser.add_argument('--ontology', dest='ontology', action='store', type=str, default=None,
                        help='the lubm ontology')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using rdftools version %s' % str_version
    else:
        lubm_generator = Lubm(ontology=args.ontology)
        print 'using LUBM classpath = ', lubm_generator.classpath
        lubm_generator(args.univ, args.index, args.seed)
        print 'done'


if __name__ == '__main__':
    main()