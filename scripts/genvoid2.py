import argparse
from rdftools.tools import NxParser
from rdftools.__version__ import str_version

__author__ = 'basca'


def main():
    parser = argparse.ArgumentParser(description='generate a VoiD descriptor using the nxparser java package')

    parser.add_argument('--data', dest='data', action='store', type=str, default=None,
                        help='the input data file to pass the NX void generator')
    parser.add_argument('--dataset_id', dest='dataset_id', action='store', type=str, default=None,
                        help='dataset id')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using rdftools version %s' % str_version
    else:
        nxparser = NxParser()
        nxparser.gen_void(args.data, args.dataset_id)
        print 'done'


if __name__ == '__main__':
    main()
