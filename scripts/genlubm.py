#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

import argparse
import time
import sys
import os
import commands
import rdftools
from multiprocessing import Pool
from rdftools.__version__ import str_version

BUNDLED_LUBM_PATH = os.path.join(os.path.split(rdftools.__file__)[0],'Uba1.7')
LUBM_ONTO = 'http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl'

#-----------------------------------------------------------------------------------------------------------------------
#
# path to lubm generator (bundled inside installed package)
#
#-----------------------------------------------------------------------------------------------------------------------
def get_lubm_path(args):
    lubm_path = BUNDLED_LUBM_PATH
    if len(args) == 1:
        lubm_path = args[0]
    elif 'LUBM_PATH' in os.environ:
        lubm_path = os.environ.get('LUBM_PATH', None)
    return BUNDLED_LUBM_PATH if not lubm_path else lubm_path

#-----------------------------------------------------------------------------------------------------------------------
#
# lubm command
#
#-----------------------------------------------------------------------------------------------------------------------
def exec_lubm(lubm_path, univ, index, seed, onto):
    status, output = commands.getstatusoutput('java -cp %s edu.lehigh.swat.bench.uba.Generator -univ %s -index %s -seed %s -onto %s'%(
        lubm_path, univ, index, seed, onto
    ))
    if status:
        print "an error occured!"
        print output

#-----------------------------------------------------------------------------------------------------------------------
#
# parallel LUBM generation
#
#-----------------------------------------------------------------------------------------------------------------------
def generate_lubm(lubm_path, univ, index, seed, onto):
    def job_finished(res):
        print '|',
        sys.stdout.flush()

    max_unis = 10 

    pool = Pool()
    for idx in xrange(index, univ+index, max_unis):
        pool.apply_async(exec_lubm,(lubm_path, max_unis, idx, seed, onto), callback = job_finished)

    pool.close()
    pool.join()



def main():
    """
    usage: genlubm.py [-h] [--univ UNIV] [--index INDEX] [--seed SEED]
                      [--ontology ONTOLOGY] [--version]

    lubm dataset generator wrapper (bundled) - requires java

    optional arguments:
      -h, --help           show this help message and exit
      --univ UNIV          number of universities to generate
      --index INDEX        start university
      --seed SEED          the seed
      --ontology ONTOLOGY  the lubm ontology by default:
                           http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl
      --version            the current version
    """
    parser = argparse.ArgumentParser(description='lubm dataset generator wrapper (bundled) - requires java')

    parser.add_argument('--univ', dest='univ', action='store', type=long, default=1,
                       help='number of universities to generate')
    parser.add_argument('--index', dest='index', action='store', type=long, default=0,
                       help='start university')
    parser.add_argument('--seed', dest='seed', action='store', type=long, default=0,
                       help='the seed')
    parser.add_argument('--ontology', dest='ontology', action='store', type=str, default=LUBM_ONTO,
                       help='the lubm ontology by default: %s'%LUBM_ONTO)
    parser.add_argument('--version', dest='version', action='store_true',
                       help='the current version')

    args = parser.parse_args()

    if args.version:
        print 'using version %s'%str_version
    else:
        lubm_path = get_lubm_path(args)
        print 'using LUBM path = ',lubm_path

        t0      = time.time()

        generate_lubm(lubm_path, args.univ, args.index, args.seed, args.ontology)
        print 'Took %s seconds'%(str(time.time()-t0))


if __name__ == '__main__':
    main()