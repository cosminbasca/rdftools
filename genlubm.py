#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from optparse import OptionParser
import time
import sys
import os
import commands
import rdftools

BUNDLED_LUBM_PATH = os.path.join(os.path.split(rdftools.__file__)[0],'Uba1.7')

def get_lubm_path(args):
    lubm_path = BUNDLED_LUBM_PATH
    if len(args) != 1:
        lubm_path = args[0]
    elif 'LUBM_PATH' in os.environ:
        lubm_path = os.environ.get('LUBM_PATH', None)

    return BUNDLED_LUBM_PATH if not lubm_path else lubm_path

def main():
    usage = "usage: %prog [options] LUBM_PATH (LUBM_PATH can also be set as an enrironment variable!)"
    parser = OptionParser(usage=usage)
    parser.add_option('-u','--univ', type='long',
                      action='store', dest='univ', default=1,
                      help='number of universities')
    parser.add_option('-i','--index', type='long',
                      action='store', dest='index', default=0,
                      help='start index')
    parser.add_option('-s','--seed', type='long',
                      action='store', dest='seed', default=0,
                      help='the seed')
    parser.add_option('-o','--onto', type='string',
                      action='store', dest='onto', default='http://www.lehigh.edu/~zhp2/2004/0401/univ-bench.owl',
                      help='ontology')

    (options, args) = parser.parse_args()

    lubm_path = get_lubm_path(args)
    print 'Using LUBM path = ',lubm_path

    t0      = time.time()
    status, output = commands.getstatusoutput('java -cp %s edu.lehigh.swat.bench.uba.Generator -univ %s -index %s -seed %s -onto %s'%(
        lubm_path, options.univ, options.index, options.seed, options.onto
    ))
    if status:
        print "an error occured!"
        print output
    print 'Took %s seconds'%(str(time.time()-t0))


if __name__ == '__main__':
    main()