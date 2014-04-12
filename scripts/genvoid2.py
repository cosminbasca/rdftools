import argparse
from rdftools.tools import NxVoid
from rdftools.__version__ import str_version

__author__ = 'basca'


def main():
    parser = argparse.ArgumentParser(description='generate a VoiD descriptor using the nxparser java package')

    parser.add_argument('source', metavar='SOURCE', type=str,
                        help='the source file to be analized')
    parser.add_argument('--dataset_id', dest='dataset_id', action='store', type=str, default=None,
                        help='dataset id')
    parser.add_argument('--version', dest='version', action='store_true',
                        help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using rdftools version %s' % str_version
    else:
        void_generator = NxVoid()
        void_generator(args.source, args.dataset_id)
        print 'done'


if __name__ == '__main__':
    main()
