import re
import argparse
from multiprocessing import Pool
import traceback
from rdftools.util import log_time
import sys
import os

__author__ = 'basca'

number_pattern = re.compile('"-?(0\.\d*[1-9]\d*|[1-9]\d*(\.\d+)?)"')

#-----------------------------------------------------------------------------------------------------------------------
#
# parallel LUBM generation
#
#-----------------------------------------------------------------------------------------------------------------------
def _round_ntfile(ntfile, round_ntfile, pattern):
    def repl(val):
        return pattern%float(val.group(0)[1:-1])

    try:
        print 'rounding "%s" -> "%s"'%(ntfile, round_ntfile)
        with open(ntfile, 'r+') as NTFILE:
            with open(round_ntfile, 'w+') as ROUND_NTFILE:
                for line in NTFILE:
                    try:
                        r_line = re.sub(number_pattern, repl, line)
                    except Exception, e:
                        print line
                        raise e
                    ROUND_NTFILE.write(r_line)

    except Exception:
        print '[fail]'
        print traceback.format_exc()
    else:
        print '[ok]'

@log_time(None)
def main():
    """
usage: dbpedia_round.py [-h] [--prefix PREFIX] [--precision PRECISION] PATH

rounds ntriple files in a folder, (rounds the floating point literals)

positional arguments:
  PATH                  location of the indexes

optional arguments:
  -h, --help            show this help message and exit
  --prefix PREFIX       the prefix used for files that are transformed, cannot
                        be the enpty string!
  --precision PRECISION
                        the precision to round to, if 0, floating point
                        numbers are rounded to floats
    """
    parser = argparse.ArgumentParser(description='rounds ntriple files in a folder, (rounds the floating point literals)')

    parser.add_argument('path', metavar='PATH', type=str,
                       help='location of the indexes')

    parser.add_argument('--prefix', dest='prefix', action='store', type=str, default='rounded',
                       help='the prefix used for files that are transformed, cannot be the enpty string!')
    parser.add_argument('--precision', dest='precision', action='store', type=long, default=0,
                       help='the precision to round to, if 0, floating point numbers are rounded to long')

    args = parser.parse_args()

    print 'running dbpedia fpoint round tool'
    if not args.prefix:
        print 'prefix cannot be empty!'
        return

    print 'rounding ... '

    pattern = '"%.'+str(args.precision)+'f"' if args.precision > 0 else '"%d"'

    if os.path.isdir(args.path):
        data_files = [ (os.path.join(args.path, dfile), os.path.join(args.path, '%s_%s'%(args.prefix, dfile)))
                       for dfile in os.listdir(args.path)
                       if not dfile.startswith('.') and os.path.splitext(dfile)[1] == ".nt" ]
    else:
        base, name = os.path.split(args.path)
        data_files = [ (os.path.join(base, name), os.path.join(base, '%s_%s'%(args.prefix, name))) ]

    pool = Pool()
    for ntfile, round_ntfile in data_files:
        pool.apply_async(_round_ntfile,(ntfile, round_ntfile, pattern, ))
    pool.close()
    pool.join()


if __name__ == '__main__':
    main()