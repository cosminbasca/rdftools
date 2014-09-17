import argparse
from pprint import pformat
from rdftools.__version__ import str_version
from rdftools.tools import Lubm, NxVoid, Void, NtFloatRounder, RaptorRdf, Rdf2Rdf, RdfEncoder
from rdftools.datagen import LubmUni2One, LubmHorizontal, LubmSeedPropagation, LubmUni2Many, DISTRIBUTIONS, \
    LubmGenerator
from rdftools.log import logger

__author__ = 'basca'

Distros = {
    'uni2one': LubmUni2One,
    'horizontal': LubmHorizontal,
    'seedprop': LubmSeedPropagation,
    'uni2many': LubmUni2Many,
}


def genlubm():
    parser = argparse.ArgumentParser(
        description='rdftools v{0}, lubm dataset generator wrapper (bundled) - requires java'.format(str_version))

    parser.add_argument('output', metavar='OUTPUT', type=str,
                        help='the location in which to save the generated distributions')
    parser.add_argument('--univ', dest='univ', action='store', type=long, default=1,
                        help='number of universities to generate')
    parser.add_argument('--index', dest='index', action='store', type=long, default=0,
                        help='start university')
    parser.add_argument('--seed', dest='seed', action='store', type=long, default=0,
                        help='the seed')
    parser.add_argument('--ontology', dest='ontology', action='store', type=str, default=None,
                        help='the lubm ontology')
    parser.add_argument('--workers', dest='workers', action='store', type=int, default=-1,
                        help='the number of workers (default -1 : all cpus)')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        logger.info('using rdftools version {0}'.format(str_version))
    else:
        lubm_generator = Lubm(ontology=args.ontology, path=args.output)
        lubm_generator(args.univ, args.index, args.seed, workers=args.workers)
        logger.info('done')


def genlubmdistro():
    parser = argparse.ArgumentParser(
        description='rdftools v{0}, lubm dataset generator wrapper (bundled) - requires java'.format(str_version))

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
    parser.add_argument('--pdist', dest='pdist', action='store', type=str, default=None,
                        help='the probabilities used for the uni2many distribution, valid choices are %s ' % DISTRIBUTIONS.keys())
    parser.add_argument('--sites', dest='sites', action='store', type=long, default=1,
                        help='the number of sites')
    parser.add_argument('--clean', dest='clean', action='store_true',
                        help='delete the generated universities')
    parser.add_argument('--workers', dest='workers', action='store', type=int, default=-1,
                        help='the number of workers (default -1 : all cpus)')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        logger.info('using rdftools version {0}'.format(str_version))
    else:
        logger.info('setup distro runner')
        _DistributionClass = Distros[args.distro]
        if not issubclass(_DistributionClass, LubmGenerator):
            raise ValueError('_DistributionClass must be a LubmGenerator')
        distro = _DistributionClass(args.output, args.sites, universities=args.univ, index=args.index, clean=args.clean,
                                    workers=args.workers, pdist=DISTRIBUTIONS.get(args.pdist, None))
        logger.info('run distribution process')
        distro()
        logger.info('done')


def genvoid():
    parser = argparse.ArgumentParser(
        description='rdftools v{0}, generate void statistics for RDF files'.format(str_version))

    parser.add_argument('source', metavar='SOURCE', type=str,
                        help='the source file to be analized')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        logger.info('using version {0}'.format(str_version))
    else:
        void_generator = Void(args.source)
        stats = void_generator()
        logger.info('Collected Statistics (VoID): \n{0}'.format(pformat(stats)))


def genvoid2():
    parser = argparse.ArgumentParser(
        description='rdftools v{0}, generate a VoiD descriptor using the nxparser java package'.format(str_version))

    parser.add_argument('source', metavar='SOURCE', type=str,
                        help='the source file to be analized')
    parser.add_argument('--dataset_id', dest='dataset_id', action='store', type=str, default=None,
                        help='dataset id')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        logger.info('using rdftools version {0}'.format(str_version))
    else:
        void_generator = NxVoid()
        void_generator(args.source, args.dataset_id)
        logger.info('done')


def ntround():
    parser = argparse.ArgumentParser(
        description='rdftools v{0}, rounds ntriple files in a folder, (rounds the floating point literals)'.format(
            str_version))

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


def rdfconvert():
    parser = argparse.ArgumentParser(
        description='rdftools v{0}, rdf converter, based on libraptor2'.format(str_version))

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
        logger.info('using version {0}'.format(str_version))
    else:
        rdf_converter = RaptorRdf()
        rdf_converter(args.source, destination_format=args.dst_format, buffer_size=args.buffer_size,
                      clear=args.clear)
        logger.info('done')


def rdfconvert2():
    parser = argparse.ArgumentParser(
        description='rdftools v{0}, rdf converter (2), makes use of rdf2rdf bundled - requires java'.format(
            str_version))

    parser.add_argument('source', metavar='SOURCE', type=str,
                        help='the source file or location (of files) to be converted')
    parser.add_argument('--clear', dest='clear', action='store_true',
                        help='clear the original files (delete) - this action is permanent, use with caution!')
    parser.add_argument('--dst_format', dest='dst_format', action='store', type=str, default='ntriples',
                        help='the destination format to convert to')
    parser.add_argument('--workers', dest='workers', action='store', type=int, default=-1,
                        help='the number of workers (default -1 : all cpus)')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        logger.info('using rdftools version {0}'.format(str_version))
    else:
        rdf_converter = Rdf2Rdf()
        rdf_converter(args.source, args.dst_format, clear_source=args.clear, workers=args.workers)
        logger.info('done')


def rdfencode():
    parser = argparse.ArgumentParser(description='rdftools v{0}, encode the RDF file(s)'.format(str_version))

    parser.add_argument('source', metavar='SOURCE', type=str,
                        help='the source file or location (of files) to be encoded')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        logger.info('using version {0}'.format(str_version))
    else:
        encoder = RdfEncoder(args.source)
        encoder()
        logger.info('done')