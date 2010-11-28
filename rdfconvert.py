#!python
__author__ = 'Cosmin Basca'
__email__ = 'basca@ifi.uzh.ch; cosmin.basca@gmail.com'

from optparse import OptionParser
import time
import sys
import os
from multiprocessing import Pool
from rdftools import *

def convert_files(files, dst_format, buffer_size):
    def job_finished(res):
        print '|',
        sys.stdout.flush()

    pool = Pool()
    for src in files:
        pool.apply_async(convert_chunked,(src, dst_format, buffer_size), callback = job_finished)

    pool.close()
    pool.join()

def main():
    usage = "usage: %prog [options] source"
    parser = OptionParser(usage=usage)
    parser.add_option('-d','--dst_fmt', type='string',
                      action='store', dest='dst_format', default='ntriples',
                      help='the RDF format of the destination file(s)')
    parser.add_option('-b','--buffer_size', type='long',
                      action='store', dest='buffer_size', default= 160,
                      help='the size in MB of the input buffer (the parser will only parse XX MB at a time)')

    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")

    t0      = time.time()
    files   = []
    src     = os.path.abspath(args[0])
    if  os.path.isdir(src):
        files = [os.path.join(src, f) for f in os.listdir(src) if supported(f) and get_parser_type(f) != options.dst_format]
    elif os.path.exists(src):
        files = [src]
    print 'To process : ',files
    convert_files(files, options.dst_format, options.buffer_size * MB)

    print 'Took %s seconds'%(str(time.time()-t0))


if __name__ == '__main__':
    main()