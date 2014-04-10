#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
from rdftools.__version__ import str_version
from rdftools.datagen import LubmUni2One, LubmHorizontal, LubmSeedPropagation, LubmUni2Many

Distros = {
    'uni2one': LubmUni2One,
    'horizontal': LubmHorizontal,
    'seedprop': LubmSeedPropagation,
    'uni2many': LubmUni2Many,
}


def main():
    parser = argparse.ArgumentParser(description='lubm dataset generator wrapper (bundled) - requires java')

    parser.add_argument('output', metavar='OUTPUT', type=str,
                        help='the location in which to save the generated distributions')
    parser.add_argument('--distro', dest='distro', action='store', type=str, default='uni2one',
                        help='the distibution to use, valid values are %s' % Distros.keys())
    parser.add_argument('--univ', dest='univ', action='store', type=long, default=1,
                        help='number of universities to generate')
    parser.add_argument('--index', dest='index', action='store', type=long, default=0,
                        help='start university')
    parser.add_argument('--seed', dest='seed', action='store', type=long, default=0,
                        help='the seed')
    parser.add_argument('--ontology', dest='ontology', action='store', type=str, default=None,
                        help='the lubm ontology')
    parser.add_argument('--sites', dest='sites', action='store', type=long, default=1,
                        help='the number of sites')
    parser.add_argument('--tmp', dest='tmp', action='store', type=str, default=None,
                        help='the location of the temporary directory')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using rdftools version %s' % str_version
    else:
        print 'setup distro runner'
        distro = Distros[args.distro](args.output, args.sites, temp_folder=args.tmp, universities=args.univ,
                                      index=args.index)
        print 'run distribution process'
        distro()
        print 'done'


if __name__ == '__main__':
    main()