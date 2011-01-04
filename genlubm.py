#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from optparse import OptionParser
import time
import sys
import os
import commands


def main():
    usage = "usage: %prog [options] LUBM_PATH"
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
    if len(args) != 1:
        parser.error("incorrect number of arguments (perhaps you did not specify the LUBM_PATH, use --help for further details)")

    t0      = time.time()
    status, output = commands.getstatusoutput('java -cp %s edu.lehigh.swat.bench.uba.Generator -univ %s -index %s -seed %s -onto %s'%(
        args[0], options.univ, options.index, options.seed, options.onto
    ))
    if status:
        print "an error occured!"
        print output
    print 'Took %s seconds'%(str(time.time()-t0))


if __name__ == '__main__':
    main()